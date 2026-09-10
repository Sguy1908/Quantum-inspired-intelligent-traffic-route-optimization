'use client'

import dynamic from 'next/dynamic'
import { useEffect, useMemo, useState } from 'react'
import { AppNavbar } from '@/components/app-navbar'
import { compareAlgorithms, runSimulation, type AlgorithmName, type ComparisonResult, type SimulationResult, type TrafficMode } from '@/lib/api'
import { ArrowRight, Check, Database, GitCompareArrows, Play, Search, Settings2, SlidersHorizontal, Sparkles } from 'lucide-react'

const RouteMap = dynamic(() => import('@/components/route-map').then(module => module.RouteMap), { ssr: false, loading: () => <div className="real-map-shell map-loading">Loading route map…</div> })

type Traffic = 'Dynamic Traffic' | 'Static Traffic'
const algorithms: Array<{ name: AlgorithmName; subtitle: string; tag: string }> = [
  { name: 'QPSO', subtitle: 'Quantum-inspired particle swarm', tag: 'Recommended' },
  { name: 'PSO', subtitle: 'Particle swarm optimization', tag: 'Baseline' },
  { name: 'GA', subtitle: 'Genetic algorithm', tag: 'Baseline' },
  { name: 'ALNS', subtitle: 'Adaptive neighborhood search', tag: 'Heuristic' },
  { name: 'Random Search', subtitle: 'Uniform random search', tag: 'Control' },
]
const trafficModes: Array<{ label: Traffic; value: TrafficMode; description: string }> = [
  { label: 'Dynamic Traffic', value: 'dynamic', description: 'Departure-time dependent travel' },
  { label: 'Static Traffic', value: 'static', description: 'Fixed edge travel times' },
]

function formatMetric(value: number | undefined, suffix = '') { return value === undefined ? '—' : `${value.toLocaleString(undefined, { maximumFractionDigits: 1 })}${suffix}` }
function metricLabel(value: number | undefined, suffix = '') { return value === undefined ? 'Awaiting run' : formatMetric(value, suffix) }
function formatDuration(minutes: number | undefined) {
  if (minutes === undefined) return 'Awaiting run'
  const seconds = Math.round(minutes * 60)
  return `${String(Math.floor(seconds / 3600)).padStart(2, '0')}:${String(Math.floor(seconds % 3600 / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`
}

export default function Page() {
  const [selected, setSelected] = useState<AlgorithmName>('QPSO')
  const [traffic, setTraffic] = useState<Traffic>('Dynamic Traffic')
  const [dark, setDark] = useState(true)
  const [search, setSearch] = useState('')
  const [seed, setSeed] = useState('12345')
  const [nodes, setNodes] = useState('50')
  const [vehicles, setVehicles] = useState('5')
  const [result, setResult] = useState<SimulationResult | null>(null)
  const [comparison, setComparison] = useState<ComparisonResult | null>(null)
  const [running, setRunning] = useState(false)
  const [compareRunning, setCompareRunning] = useState(false)
  const [error, setError] = useState('')
  useEffect(() => { document.documentElement.classList.toggle('dark', dark) }, [dark])
  const visibleAlgorithms = useMemo(() => algorithms.filter(item => item.name.toLowerCase().includes(search.toLowerCase())), [search])
  const trafficMode: TrafficMode = traffic === 'Dynamic Traffic' ? 'dynamic' : 'static'
  const scenarioReady = Number(seed) > 0 && Number(nodes) >= 20 && Number(vehicles) > 0
  const request = { traffic_mode: trafficMode, nodes: Number(nodes), vehicles: Number(vehicles), seed: Number(seed) }

  async function handleRun() {
    if (!scenarioReady) return
    setRunning(true); setError(''); setComparison(null)
    try { setResult(await runSimulation({ algorithm: selected, ...request })) } catch (err) { setError(err instanceof Error ? err.message : 'Unable to run this scenario.') } finally { setRunning(false) }
  }
  async function handleCompare() {
    if (!scenarioReady) return
    setCompareRunning(true); setError('')
    try { setComparison(await compareAlgorithms(request)) } catch (err) { setError(err instanceof Error ? err.message : 'Unable to compare algorithms.') } finally { setCompareRunning(false) }
  }

  const metrics = result?.metrics
  return <main className={dark ? 'app-shell dark-theme' : 'app-shell light-theme'}>
    <AppNavbar dark={dark} onThemeToggle={() => setDark(value => !value)} />
    <section className="workspace-intro"><div><div className="eyebrow"><Sparkles size={13} /> EXPERIMENT WORKSPACE</div><h1>Run a reproducible route study.</h1><p>Configure a seeded network, inspect one solver, or compare every method under identical traffic conditions.</p></div><div className="intro-status"><span className="status-dot" /> API configured <small>local simulation interface</small></div></section>
    <section className="dashboard-grid">
      <aside className="algorithm-panel panel"><div className="panel-heading"><div><h2>ALGORITHMS</h2><p className="section-meta">Choose a method to inspect</p></div><SlidersHorizontal size={16} /></div><label className="search-box"><Search size={16} /><input value={search} onChange={event => setSearch(event.target.value)} placeholder="Filter methods…" aria-label="Filter algorithms" /></label><div className="algorithm-list">{visibleAlgorithms.map(item => <button type="button" key={item.name} className={`algorithm-card ${selected === item.name ? 'selected' : ''}`} onClick={() => setSelected(item.name)}><div className="algorithm-title"><span className={`radio ${selected === item.name ? 'checked' : ''}`} /><div><strong>{item.name}</strong><small>{item.subtitle}</small></div><em>{selected === item.name ? <><Check size={12} /> Selected</> : item.tag}</em></div><div className="traffic-toggle">{trafficModes.map(mode => <span key={mode.label} className={traffic === mode.label && selected === item.name ? 'chosen' : ''} onClick={event => { event.stopPropagation(); setSelected(item.name); setTraffic(mode.label) }}>{mode.label.replace(' Traffic', '')}</span>)}</div></button>)}</div></aside>
      <section className="center-column"><div className="visualization panel"><div className="section-heading"><div><div className="eyebrow">LIVE ROUTE VIEW</div><h2>{selected} <span className="heading-muted">/ {traffic}</span></h2><p className="section-meta">Synthetic seeded network · scenario {seed}</p></div><span className="status-chip">{running ? 'Generating network & optimizing…' : result ? 'Run complete' : 'Ready to run'}</span></div><RouteMap algorithm={selected} traffic={traffic} result={result} /></div><div className="live-results panel"><div className="results-heading"><div><div className="eyebrow">LIVE RESULTS</div><h2>{result ? 'Scenario metrics' : 'No run loaded'}</h2></div>{result && <span className="feasibility"><span className="status-dot" /> {result.metrics.feasible ? 'Feasible route' : 'Penalized route'}</span>}</div><div className="metrics-grid">{[['Travel time', formatDuration(metrics?.travel_time_min)], ['Distance', metricLabel(metrics?.distance_km, ' km')], ['Avg speed', metricLabel(metrics?.average_speed_kmh, ' km/h')], ['Fitness', metricLabel(metrics?.fitness)], ['Convergence', result ? formatMetric(result.algorithm.convergence_percent, '%') : 'Awaiting run'], ['Nodes visited', metricLabel(metrics?.nodes_visited)], ['Total cost', metricLabel(metrics?.total_cost)]].map(([label, value]) => <div className="metric-card" key={label}><span>{label}</span><strong>{value}</strong><small>{result ? 'from current run' : 'Run a scenario to populate'}</small></div>)}</div></div>{comparison && <Comparison comparison={comparison} />}</section>
      <aside className="summary-panel panel"><div className="panel-heading"><div><div className="eyebrow"><Database size={13} /> SCENARIO BUILDER</div><h2>Seed &amp; network</h2><p className="section-meta">Keep every comparison reproducible</p></div><Settings2 size={16} /></div><div className="scenario-controls"><label>Scenario seed<input type="number" min="1" value={seed} onChange={event => setSeed(event.target.value)} /><small>Same seed = same generated network and traffic</small></label><label>Network nodes<select value={nodes} onChange={event => setNodes(event.target.value)}><option value="20">20 nodes</option><option value="50">50 nodes</option><option value="100">100 nodes</option><option value="200">200 nodes</option><option value="500">500 nodes</option></select></label><label>Vehicle fleet<select value={vehicles} onChange={event => setVehicles(event.target.value)}><option value="1">1 vehicle</option><option value="3">3 vehicles</option><option value="5">5 vehicles</option><option value="10">10 vehicles</option><option value="20">20 vehicles</option></select></label></div><div className="scenario-card"><div className="summary-title"><strong>{selected}</strong><em><span className="status-dot" />Selected</em></div><div className="summary-row"><span>Traffic model</span><strong>{traffic}</strong></div><div className="summary-row"><span>Network</span><strong>{nodes} nodes</strong></div><div className="summary-row"><span>Fleet</span><strong>{vehicles} vehicles</strong></div><div className="summary-row"><span>Evaluator</span><strong>Common traffic-aware</strong></div></div><div className="traffic-detail"><span className="status-dot" />{trafficModes.find(mode => mode.label === traffic)?.description}</div><div className="action-stack"><button type="button" className="run-button" disabled={!scenarioReady || running || compareRunning} onClick={handleRun}><Play size={15} fill="currentColor" />{running ? 'Running scenario…' : 'Run optimization'}<ArrowRight size={15} /></button><button type="button" className="compare-button" disabled={!scenarioReady || running || compareRunning} onClick={handleCompare}><GitCompareArrows size={16} />{compareRunning ? 'Comparing methods…' : 'Compare all methods'}</button></div>{error && <p className="error-message" role="alert">{error}</p>}<div className="comparison-note"><strong>Fair comparison</strong><p>One generated scenario, one traffic model, one evaluation budget. Compare All runs every solver against those same inputs.</p></div></aside>
    </section><footer>VECTRA · Vehicle &amp; Traffic Route Optimization Architecture</footer>
  </main>
}

function Comparison({ comparison }: { comparison: ComparisonResult }) {
  const ordered = comparison.results.slice().sort((a, b) => a.fitness - b.fitness)
  const maximum = Math.max(...ordered.map(item => item.fitness), 1)
  return <div className="comparison-results panel"><div className="results-heading"><div><div className="eyebrow">COMPARISON COMPLETE</div><h2>All methods, same scenario</h2></div><span className="status-chip">{ordered.length} methods</span></div><div className="comparison-table">{ordered.map((item, index) => <div className={`comparison-line ${index === 0 ? 'winner' : ''}`} key={item.name}><span className="rank">{String(index + 1).padStart(2, '0')}</span><strong>{item.name}</strong><span className="bar"><i style={{ width: `${Math.max(8, item.fitness / maximum * 100)}%` }} /></span><b>{formatMetric(item.fitness)}</b><em>{item.feasible === false ? 'Penalized' : index === 0 ? 'Best found' : 'Feasible'}</em></div>)}</div></div>
}
