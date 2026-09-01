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
│   ├── benchmarks/          # Benchmarking suite, metrics, scalability & statistical evaluation
│   └── tests/               # Unit & integration test suite
├── docs/                    # Documentation & mathematical formulations
│   └── mathematical_formulation.md
├── .gitignore               # Git ignore configuration
├── requirements.txt         # Dependencies
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

Once dependencies are installed, you can run tests and benchmarks using Python:

```bash
# Run pytest test suite
pytest

# Execute specific backend module tests
pytest tests/
```
