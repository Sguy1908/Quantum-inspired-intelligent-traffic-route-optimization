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

#### 1. Core Multi-Algorithm Benchmark Suite
Evaluates QPSO against standard PSO, Genetic Algorithm (GA), and Random Search on dynamic VRP instances:
```bash
python -m backend.benchmarks.run_benchmarks
```

#### 2. PSO vs QPSO Comparative Scaling Experiment (N = 10 to 200)
Executes multi-seed trials across problem scales to evaluate runtime scaling $R(N)$, convergence profiles $F(t)$, and relative fitness gain $\Delta F$.  Plots are generated automatically at the end of the run:
```bash
python -m backend.benchmarks.run_pso_vs_qpso_experiment
```
All generated benchmark plots (`convergence_profiles.png`, `delta_F_scaling.png`, `runtime_scaling.png`, etc.) and JSON result summaries (`experiment_results.json`, `benchmark_results.json`) are stored cleanly in `backend/benchmarks/plots/`.
