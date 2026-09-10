from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    algorithm: str = Field(default="QPSO", description="QPSO, PSO, GA, ALNS, or Random Search")
    traffic_mode: Literal["static", "dynamic"] = "dynamic"
    nodes: int = Field(default=50, ge=3, le=500)
    vehicles: int = Field(default=5, ge=1, le=50)
    seed: int = Field(default=12345, ge=1, le=2_147_483_647)
    customers: int | None = Field(default=None, ge=1, le=50)
    max_iterations: int = Field(default=40, ge=1, le=200)
    max_evaluations: int = Field(default=250, ge=10, le=2_000)
    population: int = Field(default=20, ge=2, le=100)


class ComparisonRequest(SimulationRequest):
    algorithm: str = "QPSO"


class SimulationResponse(BaseModel):
    scenario: dict
    algorithm: dict
    traffic: dict
    network: dict
    routes: list[list[int]]
    expanded_routes: list[list[int]]
    metrics: dict
    convergence_history: list[dict]


class ComparisonResponse(BaseModel):
    scenario: dict
    traffic_mode: Literal["static", "dynamic"]
    results: list[dict]
