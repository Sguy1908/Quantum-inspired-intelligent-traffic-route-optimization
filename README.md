# Quantum-Inspired Intelligent Traffic Route Optimization

An SIH 2026 Quantum Technology project implementing a Quantum-Inspired Particle Swarm Optimization (QPSO) framework for dynamic Vehicle Routing Problems (VRP).

---

## 📁 Repository Architecture

```
.
├── frontend/                # Web application UI (Reserved)
├── backend/                 # Backend system core
│   ├── graph/               # Transportation graph network & dynamic edge weight models
│   ├── simulator/           # Dynamic traffic simulation engine & re-optimization triggers
│   ├── optimizer/           # QPSO engine, random-key decoding, penalties, & baselines (PSO, GA, Exact)
│   ├── benchmarks/          # Benchmarking suite, scaling analysis, & statistical evaluation
│   │   ├── benchmark_runner.py           # Multi-trial statistical benchmark framework
│   │   ├── run_benchmarks.py             # Comprehensive multi-algorithm benchmark entrypoint
│   │   ├── run_pso_vs_qpso_experiment.py  # PSO vs QPSO scaling experiment + auto-generated plots
│   │   ├── visualization.py              # Matplotlib plotting utilities
│   │   └── plots/                        # All benchmark plots (ΔF, R(N), F(t), route maps) & results JSON
│   └── tests/               # Unit & integration test suite
├── docs/                    # Documentation & mathematical formulations
│   └── mathematical_formulation.md
├── .gitignore               # Git ignore configuration
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Virtual Environment Setup

#### Linux / macOS:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

#### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Running Tests & Benchmarks

### Unit & Integration Tests
```bash
# Run pytest test suite
pytest

# Execute specific backend module tests
pytest backend/tests/
```

### Benchmark Experiments

#### 1. Reproducible QPSO vs ALNS research benchmark

Runs paired QPSO and Adaptive Large Neighbourhood Search (ALNS) on exactly the
same saved instances and traffic scenarios in static and time-dependent modes.
Every run records raw metrics, seeds, parameters, evaluation-indexed
convergence, and the immutable instance/traffic data.

First run the small sanity configuration:

```bash
python -m backend.benchmarks.run_benchmarks --config configs/sanity_benchmark.yaml --plot
```

Then run the recorded full configuration (adjust budgets only by saving a new
configuration):

```bash
python -m backend.benchmarks.run_benchmarks --config configs/research_benchmark.yaml --plot
```

Results are written to the configured `results/` directory; `raw_results.json`
and CSV preserve each run, while `instances/` holds the exact graph, customers,
fleet, and traffic scenario. See `docs/research_audit.md` and
`docs/mathematical_formulation.md` for scope and equations.
