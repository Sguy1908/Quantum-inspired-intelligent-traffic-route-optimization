"use client"

import Link from "next/link"
import { useState } from "react"
import { ArrowRight, BookOpen, BrainCircuit, Check, ChevronRight, Code2, Compass, Cpu, GitBranch, Layers3, Map, Network, Play, Route, SlidersHorizontal, Sparkles, Workflow } from "lucide-react"
import { AppNavbar } from '@/components/app-navbar'

const sections = [
  { id: "network", label: "Network Model", icon: Network },
  { id: "formulation", label: "Formulation", icon: Code2 },
  { id: "algorithms", label: "Algorithms", icon: BrainCircuit },
  { id: "architecture", label: "Platform", icon: Layers3 },
  { id: "demo", label: "Demonstration", icon: Play },
]

const algorithmRows = [
  { name: "QPSO", full: "Quantum-behaved Particle Swarm Optimization", color: "blue", result: "24.35 km", note: "Adaptive global search", tags: ["Exploration", "Dynamic traffic"] },
  { name: "GA", full: "Genetic Algorithm", color: "green", result: "26.18 km", note: "Strong global search", tags: ["Crossover", "Complex networks"] },
  { name: "ALNS", full: "Adaptive Large Neighborhood Search", color: "purple", result: "26.92 km", note: "Large neighborhood exploration", tags: ["Destroy / repair", "Large-scale"] },
  { name: "PSO", full: "Particle Swarm Optimization", color: "orange", result: "27.43 km", note: "Fast convergence", tags: ["Swarm", "Quick solutions"] },
]

export default function TechnicalPage() {
  const [active, setActive] = useState("network")
  const [running, setRunning] = useState(false)

  return (
    <main className="technical-page">
      <AppNavbar />

      <div className="technical-layout">
        <aside className="technical-sidebar">
          <div className="eyebrow"><BookOpen size={14} /> SYSTEM NOTES</div>
          <h1>Route optimization<br /><span>from model to result.</span></h1>
          <p>Explore the network model, mathematical formulation, algorithms, and evaluation workflow behind Algo Route.</p>
          <nav className="technical-sections" aria-label="Technical sections">
            {sections.map(({ id, label, icon: Icon }) => <button className={active === id ? "active" : ""} key={id} type="button" onClick={() => setActive(id)}><Icon size={16} /><span>{label}</span><ChevronRight size={14} /></button>)}
          </nav>
          <Link href="/" className="back-dashboard"><ArrowRight size={15} /> Back to dashboard</Link>
        </aside>

        <section className="technical-content">
          <section id="network" className="tech-hero"><div className="eyebrow">TECHNICAL OVERVIEW <span>v1.4</span></div><h2>From graph topology to <em>adaptive routes.</em></h2><p>Algo Route evaluates routing algorithms against a weighted network with time-dependent traffic, operational cost, and multi-objective performance metrics.</p><div className="hero-actions"><button type="button" onClick={() => setActive("demo")} className="primary-tech-button"><Play size={15} /> View live demonstration</button><button type="button" onClick={() => setActive("formulation")} className="secondary-tech-button"><Code2 size={15} /> Read formulation</button></div></section>

          <section className="tech-grid network-grid">
            <article className="tech-panel wide-panel"><div className="panel-topline"><span className="section-number">01</span><div><div className="eyebrow">NETWORK MODEL</div><h3>A directed, time-dependent graph</h3></div></div><div className="network-diagram"><div className="diagram-grid" /><div className="network-edge edge-a" /><div className="network-edge edge-b" /><div className="network-edge edge-c" /><div className="network-edge edge-d" /><div className="network-edge edge-e" /><span className="network-node node-a">S</span><span className="network-node node-b">1</span><span className="network-node node-c">2</span><span className="network-node node-d">3</span><span className="network-node node-e">4</span><span className="network-node node-f">T</span><div className="diagram-caption"><span><i className="legend-line route-line" /> Selected route</span><span><i className="legend-line alt-line" /> Candidate edges</span></div></div><p className="panel-copy">Each road segment is modeled as an edge with a distance, travel time, cost, and congestion state. The route is a sequence of connected edges between a source <code>S</code> and destination <code>T</code>.</p></article>
            <article className="tech-panel compact-panel"><span className="panel-icon"><Compass size={18} /></span><div className="eyebrow">INPUT SIGNALS</div><h3>Four weighted dimensions</h3><ul className="signal-list"><li><span className="signal-dot blue" /> Distance <strong>km</strong></li><li><span className="signal-dot green" /> Travel time <strong>min</strong></li><li><span className="signal-dot orange" /> Operating cost <strong>USD</strong></li><li><span className="signal-dot purple" /> Congestion <strong>0–1</strong></li></ul></article>
          </section>

          <section id="formulation" className="tech-panel formulation-panel"><div className="panel-topline"><span className="section-number">02</span><div><div className="eyebrow">FORMULATION</div><h3>Optimize the route, not one metric</h3></div><span className="formula-status"><Check size={13} /> constrained</span></div><div className="formula-layout"><div className="formula-block"><span className="formula-label">OBJECTIVE FUNCTION</span><div className="formula-display">min <span>J(R)</span> = <span>α</span> · D(R) + <span>β</span> · T(R) + <span>γ</span> · C(R)</div><p>Weighted objectives balance distance, travel time, and operational cost according to the active scenario.</p></div><div className="constraint-block"><span className="formula-label">CONSTRAINTS</span><div className="constraint-row"><span>Flow continuity</span><code>∑xᵢⱼ − ∑xⱼₖ = bⱼ</code></div><div className="constraint-row"><span>Binary edge choice</span><code>xᵢⱼ ∈ {'{'}0, 1{'}'}</code></div><div className="constraint-row"><span>Time windows</span><code>tᵢ ≤ arrivalᵢ ≤ t̄ᵢ</code></div></div></div></section>

          <section id="algorithms" className="algorithms-section"><div className="section-heading-row"><div><div className="eyebrow">03 / ALGORITHMS</div><h3>One problem. Four search strategies.</h3></div><span className="section-aside">Dynamic traffic benchmark</span></div><div className="algorithm-table">{algorithmRows.map((row, index) => <article className="algorithm-row" key={row.name}><span className={`algorithm-rank rank-${row.color}`}>0{index + 1}</span><div className="algorithm-name"><strong>{row.name}</strong><span>{row.full}</span></div><div className="algorithm-tags">{row.tags.map(tag => <span key={tag}>{tag}</span>)}</div><div className="algorithm-result"><strong>{row.result}</strong><span>{row.note}</span></div></article>)}</div></section>

          <section id="architecture" className="tech-grid architecture-grid"><article className="tech-panel architecture-panel"><div className="panel-topline"><span className="section-number">04</span><div><div className="eyebrow">PLATFORM</div><h3>Composable evaluation pipeline</h3></div></div><div className="pipeline"><div><Cpu size={16} /><span>Scenario<br />builder</span></div><i /><div><GitBranch size={16} /><span>Algorithm<br />runner</span></div><i /><div><SlidersHorizontal size={16} /><span>Metric<br />engine</span></div><i /><div><Sparkles size={16} /><span>Route<br />insights</span></div></div></article><article className="tech-panel metrics-panel"><div className="eyebrow">REPORTED METRICS</div><h3>Performance, made legible.</h3><div className="metric-chips"><span>Distance</span><span>Time</span><span>Cost</span><span>Convergence</span><span>Fitness</span></div></article></section>

          <section id="demo" className="demo-panel"><div className="demo-copy"><div className="eyebrow">05 / DEMONSTRATION</div><h3>Replay the benchmark scenario.</h3><p>Watch the selected route converge through the network while the evaluation metrics update in real time.</p><button type="button" className="primary-tech-button" onClick={() => { setRunning(true); window.setTimeout(() => setRunning(false), 3600) }}><Play size={15} /> {running ? "Simulation running" : "Run simulation"}</button></div><div className={`demo-visual ${running ? "is-running" : ""}`}><div className="demo-map-grid" /><div className="demo-route route-one" /><div className="demo-route route-two" /><span className="demo-pin pin-start">S</span><span className="demo-pin pin-end">T</span><div className="demo-readout"><span className="status-dot" /> {running ? "Optimizing route…" : "Ready to simulate"}<strong>{running ? "Iteration 42 / 100" : "QPSO / Dynamic"}</strong></div></div></section>
        </section>
      </div>
    </main>
  )
}
