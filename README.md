# Quantum-Inspired Intelligent Traffic Route Optimization

An SIH 2026 Quantum Technology project implementing a Quantum-Inspired Particle Swarm Optimization (QPSO) framework for dynamic Vehicle Routing Problems (VRP).

---

## 📁 Repository Architecture

```
.
├── frontend/                # Web application UI (Reserved - untouched)
├── backend/                 # Backend system core
│   ├── graph/               # Transportation graph network & dynamic edge weight models
│   ├── simulator/           # Dynamic traffic simulation engine & re-optimization triggers
│   ├── optimizer/           # QPSO engine, random-key decoding, penalties, & baselines (PSO, GA, Exact)
│   └── benchmarks/          # Benchmarking suite, metrics, scalability & statistical evaluation
├── docs/                    # Documentation & mathematical formulations
│   └── mathematical_formulation.md
├── tests/                   # Unit & integration test suite
├── requirements.txt         # Dependencies
└── README.md
```

---

## 🚀 Getting Started

All simulator and optimization backend modules reside entirely inside `backend/`.
