'use client'

import dynamic from 'next/dynamic'
import { useEffect, useState } from 'react'
import { AppNavbar } from '@/components/app-navbar'
import { Check, Search, Sun } from 'lucide-react'

const RouteMap = dynamic(() => import('@/components/route-map').then((module) => module.RouteMap), { ssr: false, loading: () => <div className="real-map-shell map-loading">Loading route map…</div> })
type Traffic = 'Dynamic Traffic' | 'Static Traffic'
const algorithms = [
  ['QPSO', 'Quantum-Inspired Particle Swarm Optimization'],
  ['PSO', 'Particle Swarm Optimization'],
  ['GA', 'Genetic Algorithm'],
  ['ALNS', 'Adaptive Large Neighborhood Search'],
  ['Random Search', 'Uniform Random Search'],
] as const

export default function Page() {
  const [selected, setSelected] = useState<(typeof algorithms)[number][0]>('QPSO')
  const [traffic, setTraffic] = useState<Traffic>('Dynamic Traffic')
  const [dark, setDark] = useState(true)
  useEffect(() => { document.documentElement.classList.toggle('dark', dark) }, [dark])
  return <main className={dark ? 'app-shell dark-theme' : 'app-shell light-theme'}>
    <AppNavbar dark={dark} onThemeToggle={() => setDark(value => !value)} />
    <section className="dashboard-grid">
      <aside className="algorithm-panel panel"><div className="panel-heading"><div><h2>ALGORITHMS</h2><p className="section-meta">Benchmark methods</p></div></div><label className="search-box"><Search size={17} /><input placeholder="Search algorithms…" aria-label="Search algorithms" /></label><div className="algorithm-list">{algorithms.map(([name, subtitle]) => <button key={name} className={`algorithm-card ${selected === name ? 'selected' : ''}`} onClick={() => setSelected(name)}><div className="algorithm-title"><span className={`radio ${selected === name ? 'checked' : ''}`} /><div><strong>{name}</strong><small>{subtitle}</small></div>{selected === name && <em><Check size={12} /> Active</em>}</div><div className="traffic-toggle">{(['Dynamic Traffic', 'Static Traffic'] as Traffic[]).map(mode => <span key={mode} className={traffic === mode && selected === name ? 'chosen' : ''} onClick={event => { event.stopPropagation(); setSelected(name); setTraffic(mode) }}>{mode}</span>)}</div></button>)}</div></aside>
      <section className="center-column"><div className="visualization panel"><div className="section-heading"><div><h2>ROUTE VISUALIZATION</h2><p className="section-meta">Jaipur → Ajmer NH 48 · {selected} · {traffic}</p></div><span className="status-chip">{traffic}</span></div><RouteMap algorithm={selected} traffic={traffic} /></div><div className="overview panel"><h2>RESEARCH SCOPE</h2><div className="overview-grid"><div className="overview-card"><span>Problem</span><strong>Traffic-aware CVRPTW</strong><small>Directed weighted graph</small></div><div className="overview-card"><span>Network sizes</span><strong>20–500 nodes</strong><small>20, 50, 100, 200, 300, 400, 500</small></div><div className="overview-card"><span>Evaluation budget</span><strong>5,000</strong><small>Objective evaluations / run</small></div><div className="overview-card"><span>Iterations</span><strong>1,000</strong><small>Maximum / run</small></div></div></div></section>
      <aside className="summary-panel panel"><h2>SCENARIO</h2><div className="summary-card"><div className="summary-title"><strong>{selected}</strong><em><span className="status-dot" />Selected</em></div><div className="summary-row"><span>Traffic model</span><strong>{traffic}</strong></div><div className="summary-row"><span>Route</span><strong>Jaipur → Ajmer</strong></div><div className="summary-row"><span>Evaluator</span><strong>Common</strong></div><div className="summary-row"><span>Results</span><strong>Benchmark pending</strong></div></div><div className="comparison"><h3>EXPERIMENT DESIGN</h3><p>Static and dynamic traffic conditions are evaluated across the same instances, scenarios, objective function, penalties, and budget.</p></div></aside>
    </section><footer>VECTRA · Vehicle &amp; Traffic Route Optimization Architecture</footer>
  </main>
}
