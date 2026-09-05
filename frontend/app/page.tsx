'use client'

import { useEffect, useMemo, useState } from 'react'
import { ArrowRight, Check, ChevronDown, ChevronRight, CircleDollarSign, Clock3, Menu, Network, Route, Search, SlidersHorizontal, Sun, Target, TrendingUp, Zap } from 'lucide-react'

type Traffic = 'Dynamic Traffic' | 'Static Traffic'
type Algorithm = { name: string; subtitle: string; description: string; color: string }
type Metric = { label: string; value: string; color: string; type: string }

const algorithms: Algorithm[] = [
  { name: 'QPSO', subtitle: 'Quantum-behaved Particle Swarm Optimization', description: 'Adapts to changing traffic conditions.', color: 'blue' },
  { name: 'GA', subtitle: 'Genetic Algorithm', description: 'Strong global search for optimal routes.', color: 'slate' },
  { name: 'ALNS', subtitle: 'Adaptive Large Neighborhood Search', description: 'Adaptive exploration for large networks.', color: 'slate' },
  { name: 'PSO', subtitle: 'Particle Swarm Optimization', description: 'Fast convergence and simple execution.', color: 'slate' },
]

const baseMetrics: Record<string, { distance: number; time: string; speed: string; cost: string; nodes: string; convergence: string; fitness: string }> = {
  QPSO: { distance: 24.35, time: '00:56:32', speed: '25.8 km/h', cost: '$ 12.40', nodes: '48', convergence: '92.6 %', fitness: '0.947' },
  GA: { distance: 26.18, time: '01:02:10', speed: '24.1 km/h', cost: '$ 13.25', nodes: '52', convergence: '88.4 %', fitness: '0.914' },
  ALNS: { distance: 26.92, time: '01:04:28', speed: '23.7 km/h', cost: '$ 13.76', nodes: '55', convergence: '86.9 %', fitness: '0.899' },
  PSO: { distance: 27.43, time: '01:06:17', speed: '23.2 km/h', cost: '$ 14.02', nodes: '57', convergence: '84.8 %', fitness: '0.881' },
}

function LogoMark() { return <div className="logo-mark"><Network size={33} strokeWidth={1.8} /><span className="logo-dot dot-one" /><span className="logo-dot dot-two" /><span className="logo-dot dot-three" /></div> }
function MetricIcon({ type }: { type: string }) { const props = { size: 19, strokeWidth: 1.8 }; if (type === 'time') return <Clock3 {...props} />; if (type === 'nodes') return <Network {...props} />; if (type === 'speed') return <TrendingUp {...props} />; if (type === 'cost') return <CircleDollarSign {...props} />; if (type === 'fitness') return <Target {...props} />; return <Route {...props} /> }

function MapCanvas({ algorithm, traffic }: { algorithm: string; traffic: Traffic }) {
  const dynamic = traffic === 'Dynamic Traffic'
  return <div className={`map-canvas ${dynamic ? 'is-dynamic' : 'is-static'}`} aria-label={`${algorithm} ${traffic} route map`}>
    <div className="map-water water-one" /><div className="map-water water-two" /><div className="map-water water-three" />
    <div className="map-road road-one traffic-normal" /><div className="map-road road-two traffic-heavy" /><div className="map-road road-three traffic-moderate" /><div className="map-road road-four traffic-moderate" />
    <div className="map-route route-alternative route-alt-one" /><div className="map-route route-alternative route-alt-two" />
    <div className="map-route route-green" /><div className="map-route route-blue" /><div className="map-route route-red" />
    <div className="traffic-dots dots-one"><i /><i /><i /></div><div className="traffic-dots dots-two"><i /><i /><i /></div><div className="traffic-dots dots-three"><i /><i /><i /></div>
    <div className="route-nodes green-nodes"><i /><i /><i /><i /><i /><i /></div><div className="route-nodes blue-nodes"><i /><i /><i /><i /></div><div className="route-nodes red-nodes"><i /><i /><i /><i /><i /></div>
    <div className="pin start-pin"><span>START</span></div><div className="pin end-pin"><span>END</span></div>
    <div className="map-status"><span className="status-dot" />{dynamic ? 'LIVE TRAFFIC' : 'STATIC TRAFFIC'} <small>• {algorithm} route engine</small></div>
    <div className="map-legend"><span><b className="legend-green" />Free flow</span><span><b className="legend-yellow" />Moderate</span><span><b className="legend-red" />Congested</span></div>
  </div>
}

export default function Page() {
  const [selected, setSelected] = useState('QPSO')
  const [traffic, setTraffic] = useState<Traffic>('Dynamic Traffic')
  const [dark, setDark] = useState(true)
  const metrics = useMemo(() => baseMetrics[selected], [selected])
  const factor = traffic === 'Static Traffic' ? 1.225 : 1
  const distance = (metrics.distance * factor).toFixed(2)
  const overview: [string, string, string][] = [['Total Distance', `${distance} km`, 'route'], ['Total Time', metrics.time, 'time'], ['Nodes Visited', metrics.nodes, 'nodes'], ['Avg Speed', metrics.speed, 'speed'], ['Total Cost', metrics.cost, 'cost'], ['Fitness Score', metrics.fitness, 'fitness']]
  const summary: Metric[] = [['Total Distance', `${distance} km`, 'blue', 'route'], ['Total Time', metrics.time, 'green', 'time'], ['Avg Speed', metrics.speed, 'orange', 'speed'], ['Total Cost', metrics.cost, 'orange', 'cost'], ['Nodes Visited', metrics.nodes, 'purple', 'nodes'], ['Convergence', metrics.convergence, 'blue', 'route'], ['Fitness Score', metrics.fitness, 'pink', 'fitness']].map(([label, value, color, type]) => ({ label, value, color, type }))
  const comparisons = algorithms.map((algorithm, index) => { const value = baseMetrics[algorithm.name].distance * factor; return [`${algorithm.name} (${traffic.split(' ')[0]})`, `${value.toFixed(2)} km`, ['blue', 'purple', 'orange', 'teal'][index], Math.max(42, 76 - index * 7)] as const })
  useEffect(() => { document.documentElement.classList.toggle('dark', dark) }, [dark])

  return <main className={dark ? 'app-shell dark-theme' : 'app-shell light-theme'}>
    <header className="topbar"><div className="brand"><LogoMark /><div><strong>ALGO ROUTE</strong><small>Route Optimization &amp; Traffic Simulation</small><em>Team Atlas · v1.0</em></div></div><nav className="primary-nav" aria-label="Product navigation"><button className="active"><Zap size={19} />Simulation</button></nav><div className="system-identity"><span className="status-dot" />System ready</div><div className="top-actions"><button className="theme-toggle" onClick={() => setDark((value) => !value)} aria-label={`Switch to ${dark ? 'light' : 'dark'} theme`}><Sun size={20} /></button><button className="mobile-menu" aria-label="Open navigation"><Menu size={20} /></button></div></header>
    <section className="dashboard-grid"><aside className="algorithm-panel panel"><div className="panel-heading"><div><h2>ALGORITHMS</h2><p className="section-meta">Select a route solver</p></div><SlidersHorizontal size={19} /></div><label className="search-box"><Search size={17} /><input placeholder="Search algorithms..." aria-label="Search algorithms" /></label><div className="algorithm-list">{algorithms.map((algorithm) => <button key={algorithm.name} className={`algorithm-card ${selected === algorithm.name ? 'selected' : ''}`} onClick={() => setSelected(algorithm.name)}><div className="algorithm-title"><span className={`radio ${selected === algorithm.name ? 'checked' : ''}`} /><div><strong>{algorithm.name}</strong><small>{algorithm.subtitle}</small></div>{selected === algorithm.name && <em><Check size={12} /> Active</em>}</div><div className="traffic-toggle">{(['Dynamic Traffic', 'Static Traffic'] as Traffic[]).map((mode) => <span key={mode} className={traffic === mode && selected === algorithm.name ? 'chosen' : ''} onClick={(event) => { event.stopPropagation(); setSelected(algorithm.name); setTraffic(mode) }}>{mode}</span>)}</div><p>{algorithm.description}</p></button>)}</div></aside>
      <section className="center-column"><div className="visualization panel"><div className="section-heading"><div><h2>ROUTE VISUALIZATION</h2><p className="section-meta">{traffic === 'Dynamic Traffic' ? 'Live simulation updating' : 'Stable traffic baseline'} · {selected} engine</p></div><div className="viz-actions"><button className="select-button">{selected} ({traffic.split(' ')[0]}) <ChevronDown size={16} /></button><button aria-label="Visualization settings"><SlidersHorizontal size={17} />Compare</button></div></div><MapCanvas algorithm={selected} traffic={traffic} /></div><div className="overview panel"><h2>ROUTE OVERVIEW</h2><div className="overview-grid">{overview.map(([label, value, type]) => <div className="overview-card" key={label}><div className={`metric-icon icon-${type}`}><MetricIcon type={type} /></div><span>{label}</span><strong>{value}</strong><small>Best: {selected}</small></div>)}<button className="details-button">View Detailed Results <ArrowRight size={17} /></button></div></div></section>
      <aside className="summary-panel panel"><h2>SUMMARY</h2><div className="summary-card"><div className="summary-title"><strong>{selected} <span>({traffic})</span></strong><em><span className="status-dot" />Active</em></div>{summary.map((item) => <div className="summary-row" key={item.label}><i className={`metric-${item.color}`}><MetricIcon type={item.type} /></i><span>{item.label}</span><strong>{item.value}</strong></div>)}</div><div className="comparison"><h3>BEST COMPARISON <small>(Distance)</small></h3>{comparisons.map(([label, value, color, width]) => <div className="comparison-row" key={label}><span>{label}</span><div className="comparison-bar"><i className={`bar-${color}`} style={{ width: `${width}%` }} /></div><strong>{value}</strong></div>)}</div></aside></section><footer>© 2025 Algo Route. All rights reserved.</footer>
  </main>
}
