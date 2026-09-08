'use client'

import dynamic from 'next/dynamic'
import { useEffect, useMemo, useState } from 'react'
import { AppNavbar } from '@/components/app-navbar'
import { compareAlgorithms, runSimulation, type ComparisonResult, type SimulationResult, type TrafficMode } from '@/lib/api'
import { Check, Play, RefreshCw, Search } from 'lucide-react'

const RouteMap = dynamic(() => import('@/components/route-map').then((module) => module.RouteMap), { ssr: false, loading: () => <div className="real-map-shell map-loading">Loading route map…</div> })
type Traffic = 'Dynamic Traffic' | 'Static Traffic'
const algorithms = [
  ['QPSO', 'Quantum-Inspired Particle Swarm Optimization'],
  ['PSO', 'Particle Swarm Optimization'],
  ['GA', 'Genetic Algorithm'],
  ['ALNS', 'Adaptive Large Neighborhood Search'],
  ['Random Search', 'Uniform Random Search'],
] as const

const asMode = (traffic: Traffic): TrafficMode => traffic === 'Dynamic Traffic' ? 'dynamic' : 'static'
const formatTime = (minutes: number) => {
  const totalSeconds = Math.round(minutes * 60); const hours = Math.floor(totalSeconds / 3600); const mins = Math.floor((totalSeconds % 3600) / 60); const seconds = totalSeconds % 60
  return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

export default function Page() {
  const [selected, setSelected] = useState<(typeof algorithms)[number][0]>('QPSO')
  const [traffic, setTraffic] = useState<Traffic>('Dynamic Traffic')
  const [dark, setDark] = useState(true)
  const [query, setQuery] = useState('')
  const [seed, setSeed] = useState(12345)
  const [nodes, setNodes] = useState(50)
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [comparison, setComparison] = useState<ComparisonResult | null>(null)
  const [runState, setRunState] = useState<'idle' | 'running' | 'success' | 'error'>('idle')
  const [comparisonRunning, setComparisonRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => { document.documentElement.classList.toggle('dark', dark) }, [dark])
  const filteredAlgorithms = useMemo(() => algorithms.filter(([name, subtitle]) => `${name} ${subtitle}`.toLowerCase().includes(query.toLowerCase())), [query])

  const run = async () => {
    setRunState('running'); setError(null); setComparison(null)
    try {
      const output = await runSimulation({ algorithm: selected, traffic_mode: asMode(traffic), nodes, vehicles: 1, seed })
      setResult(output); setRunState('success')
    } catch (caught) { setError(caught instanceof Error ? caught.message : 'The simulation could not be completed.'); setRunState('error') }
  }
  const compare = async () => {
    setComparisonRunning(true); setError(null)
    try { setComparison(await compareAlgorithms({ traffic_mode: asMode(traffic), nodes, vehicles: 1, seed })) }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'The comparison could not be completed.') }
    finally { setComparisonRunning(false) }
  }
  const metrics = result?.metrics
  const metricCards = metrics ? [
    ['Total Distance', `${metrics.distance_km.toFixed(2)} km`, 'Returned route edges'],
    ['Total Time', formatTime(metrics.travel_time_min), 'Traffic-aware traversal'],
    ['Avg Speed', `${metrics.average_speed_kmh.toFixed(1)} km/h`, 'Across travelled edges'],
    ['Total Cost', `$${metrics.total_cost.toFixed(2)}`, 'Simulation edge cost'],
    ['Nodes Visited', String(metrics.nodes_visited), `${result?.scenario.customers.length ?? 0} customers`],
    ['Fitness Score', metrics.fitness.toFixed(3), metrics.feasible ? 'Feasible best solution found' : 'Constraint violation'],
  ] : [
    ['Total Distance', '—', 'Run a scenario'], ['Total Time', '—', 'Run a scenario'], ['Avg Speed', '—', 'Run a scenario'],
    ['Total Cost', '—', 'Run a scenario'], ['Nodes Visited', '—', 'Run a scenario'], ['Fitness Score', '—', 'Run a scenario'],
  ]

  return <main className={dark ? 'app-shell dark-theme' : 'app-shell light-theme'}>
    <AppNavbar dark={dark} onThemeToggle={() => setDark(value => !value)} />
    <section className="dashboard-grid">
      <aside className="algorithm-panel panel"><div className="panel-heading"><div><h2>ALGORITHMS</h2><p className="section-meta">Live metaheuristic methods</p></div></div>
        <label className="search-box"><Search size={17} /><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Search algorithms…" aria-label="Search algorithms" /></label>
        <div className="algorithm-list">{filteredAlgorithms.map(([name, subtitle]) => <button key={name} className={`algorithm-card ${selected === name ? 'selected' : ''}`} onClick={() => setSelected(name)}><div className="algorithm-title"><span className={`radio ${selected === name ? 'checked' : ''}`} /><div><strong>{name}</strong><small>{subtitle}</small></div>{selected === name && <em><Check size={12} /> Active</em>}</div><div className="traffic-toggle">{(['Dynamic Traffic', 'Static Traffic'] as Traffic[]).map(mode => <span key={mode} role="button" tabIndex={0} className={traffic === mode && selected === name ? 'chosen' : ''} onClick={event => { event.stopPropagation(); setSelected(name); setTraffic(mode) }} onKeyDown={event => { if (event.key === 'Enter' || event.key === ' ') { event.stopPropagation(); setSelected(name); setTraffic(mode) } }}>{mode}</span>)}</div></button>)}</div>
        <div className="run-controls"><label>Seed<input type="number" value={seed} min={0} onChange={event => setSeed(Math.max(0, Number(event.target.value) || 0))} /></label><label>Network nodes<input type="number" value={nodes} min={6} max={200} onChange={event => setNodes(Math.min(200, Math.max(6, Number(event.target.value) || 6)))} /></label></div>
        <button className="run-button" onClick={run} disabled={runState === 'running'}>{runState === 'running' ? <RefreshCw className="spin" size={17} /> : <Play size={17} />}{runState === 'running' ? `Running ${selected}…` : 'RUN OPTIMIZATION'}</button>
      </aside>
      <section className="center-column"><div className="visualization panel"><div className="section-heading"><div><h2>ROUTE VISUALIZATION</h2><p className="section-meta">{result ? `Seed ${result.scenario.seed} · ${result.network.nodes.length}-node network · ${result.algorithm.name} · ${result.traffic.mode} traffic` : `Select ${selected} · ${traffic} · then RUN`}</p></div><span className="status-chip">{runState === 'running' ? 'Executing backend…' : runState === 'success' ? 'Best solution found' : traffic}</span></div><RouteMap result={result} /></div>
        {error && <div className="api-error" role="alert">{error}</div>}
        <div className="overview panel"><h2>LIVE RESULTS</h2><div className="overview-grid">{metricCards.map(([label, value, detail]) => <div className="overview-card" key={label}><span>{label}</span><strong>{value}</strong><small>{detail}</small></div>)}</div></div>
      </section>
      <aside className="summary-panel panel"><h2>SCENARIO</h2><div className="summary-card"><div className="summary-title"><strong>{selected}</strong><em><span className="status-dot" />{runState === 'success' ? 'Complete' : runState === 'running' ? 'Running' : 'Selected'}</em></div><div className="summary-row"><span>Traffic model</span><strong>{traffic}</strong></div><div className="summary-row"><span>Scenario seed</span><strong>{result?.scenario.seed ?? seed}</strong></div><div className="summary-row"><span>Network</span><strong>{result ? `${result.scenario.nodes} nodes / ${result.scenario.edges} edges` : `${nodes} nodes`}</strong></div><div className="summary-row"><span>Evaluator</span><strong>Common traffic-aware</strong></div><div className="summary-row"><span>Iterations</span><strong>{result?.algorithm.iterations ?? '—'}</strong></div><div className="summary-row"><span>Convergence</span><strong>{result ? `${result.algorithm.convergence_percent.toFixed(1)}%` : '—'}</strong></div></div>
        <div className="comparison"><h3>BEST COMPARISON <small>same scenario only</small></h3>{comparison ? comparison.results.map((item, index) => <div className="comparison-row" key={item.name}><strong>{item.name}</strong><div className="comparison-bar"><i className={index === 0 ? 'bar-blue' : index === 1 ? 'bar-purple' : index === 2 ? 'bar-orange' : 'bar-teal'} style={{ width: `${Math.max(8, Math.min(100, comparison.results[0].fitness / item.fitness * 100))}%` }} /></div><span>{item.fitness.toFixed(1)}</span></div>) : <p>Run a paired comparison to evaluate all algorithms on seed {seed} under identical traffic and constraints.</p>}<button className="compare-button" disabled={comparisonRunning || runState === 'running'} onClick={compare}>{comparisonRunning ? <><RefreshCw className="spin" size={15} /> Comparing…</> : 'COMPARE ALL'}</button></div>
      </aside>
    </section><footer>VECTRA · Vehicle &amp; Traffic Route Optimization Architecture</footer>
  </main>
}
