from __future__ import annotations
import sys
import os
from fastapi import APIRouter, HTTPException

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)


from backend.api.schemas import ComparisonRequest, ComparisonResponse, SimulationRequest, SimulationResponse
from backend.scenarios.generator import build_scenario, serialize_simulation

router = APIRouter(prefix="/api", tags=["simulation"])

ALGORITHMS = {
    "qpso": ("qpso", "QPSO"),
    "pso": ("pso", "PSO"),
    "ga": ("ga", "GA"),
    "alns": ("alns", "ALNS"),
    "random": ("random", "Random Search"),
    "random search": ("random", "Random Search"),
    "random_search": ("random", "Random Search"),
}


def _algorithm(value: str) -> tuple[str, str]:
    normalized = value.strip().lower()
    if normalized not in ALGORITHMS:
        raise HTTPException(status_code=422, detail="algorithm must be one of QPSO, PSO, GA, ALNS, or Random Search")
    return ALGORITHMS[normalized]


def _scenario_from_request(request: SimulationRequest):
    try:
        return build_scenario(seed=request.seed, nodes=request.nodes, vehicles=request.vehicles,
                              traffic_mode=request.traffic_mode, customers=request.customers)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


def _run(request: SimulationRequest, scenario=None) -> dict:
    algorithm_key, algorithm_label = _algorithm(request.algorithm)
    scenario = scenario or _scenario_from_request(request)
    try:
        result = scenario.simulator.run_optimizer(
            algorithm=algorithm_key,
            max_iterations=request.max_iterations,
            num_particles=request.population,
            max_evaluations=request.max_evaluations,
            seed=request.seed,
        )
        return serialize_simulation(scenario, algorithm_label, result)
    except Exception as error:  # convert solver failures into a client-visible API error
        raise HTTPException(status_code=500, detail=f"{algorithm_label} optimisation failed: {error}") from error


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/simulation/run", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest) -> dict:
    return _run(request)


@router.post("/simulation/compare", response_model=ComparisonResponse)
def compare_algorithms(request: ComparisonRequest) -> dict:
    scenario = _scenario_from_request(request)
    results = []
    scenario_payload = None
    # One scenario instance is intentionally shared.  Optimisers have their
    # own seeded RNG but see identical graph, customers, fleet, and traffic.
    for key, label in (("qpso", "QPSO"), ("pso", "PSO"), ("ga", "GA"), ("alns", "ALNS"), ("random", "Random Search")):
        payload = _run(request.model_copy(update={"algorithm": key}), scenario)
        if scenario_payload is None:
            scenario_payload = payload["scenario"]
        metrics = payload["metrics"]
        results.append({
            "name": label,
            "fitness": metrics["fitness"],
            "feasible": metrics["feasible"],
            "distance_km": metrics["distance_km"],
            "travel_time_min": metrics["travel_time_min"],
            "total_cost": metrics["total_cost"],
            "runtime_ms": payload["algorithm"]["runtime_ms"],
            "objective_evaluations": payload["algorithm"]["objective_evaluations"],
        })
    return {"scenario": scenario_payload, "traffic_mode": request.traffic_mode, "results": results}


# Compatibility aliases keep the existing API client usable while it migrates
# to the explicit simulation namespace.
@router.post("/simulate", response_model=SimulationResponse, include_in_schema=False)
def legacy_run_simulation(request: SimulationRequest) -> dict:
    return _run(request)


@router.post("/compare", response_model=ComparisonResponse, include_in_schema=False)
def legacy_compare_algorithms(request: ComparisonRequest) -> dict:
    return compare_algorithms(request)
