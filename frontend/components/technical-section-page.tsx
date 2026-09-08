"use client"

import dynamic from "next/dynamic"
import { useState } from "react"
import { AppNavbar } from "@/components/app-navbar"
import { ArrowRight, BookOpen, BrainCircuit, Check, Code2, Cpu, GitBranch, Layers3, Network, Route, Workflow } from "lucide-react"

const RouteMap = dynamic(() => import('@/components/route-map').then(module => module.RouteMap), { ssr: false, loading: () => <div className="real-map-shell map-loading">Loading route map…</div> })
type PageKey = 'network-model' | 'formulation' | 'algorithms' | 'platform' | 'demonstration'
const pageData: Record<PageKey, { eyebrow: string; title: string; intro: string }> = {
  'network-model': { eyebrow: '01 / NETWORK MODEL', title: 'Directed weighted transportation graph', intro: 'The transportation network is modeled as G = (V, E). Node 0 is the depot; remaining nodes represent customer locations; directed edges represent road segments.' },
  formulation: { eyebrow: '02 / FORMULATION', title: 'Traffic-aware CVRPTW', intro: 'The objective minimizes routing cost under departure-time-dependent travel times, vehicle capacity, time windows, flow conservation, and depot constraints.' },
  algorithms: { eyebrow: '03 / ALGORITHMS', title: 'Five benchmark methods', intro: 'QPSO, PSO, GA, Random Search, and ALNS use the same instances, traffic scenarios, evaluator, penalties, and evaluation budget.' },
  platform: { eyebrow: '04 / PLATFORM', title: 'Research implementation architecture', intro: 'The implementation separates the transportation graph, route evaluator, optimizer implementations, benchmark runner, aggregation, and visualization.' },
  demonstration: { eyebrow: '05 / DEMONSTRATION', title: 'Demonstration outputs', intro: 'Uploaded experimental images are shown without modification. Numerical benchmark claims remain pending until supplied outputs are available.' },
}
const algorithms = [['QPSO', 'Quantum-inspired Particle Swarm Optimization'], ['PSO', 'Particle Swarm Optimization'], ['GA', 'Genetic Algorithm'], ['ALNS', 'Adaptive Large Neighborhood Search'], ['Random Search', 'Uniform Random Search']]
const demonstrationFigures = [
  ['Static traffic convergence (all raw runs)', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-j9vXbKUh87bbhvuctDRPcLv8u8DorF.png'],
  ['Static traffic: Constraint violation', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-HULlXlBXok4LeKQg32TF9YHQ3YfbH2.png'],
  ['Dynamic traffic: Objective', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-TB8eOrVEutPkYhyiXpkL5zO2QCMsOv.png'],
  ['Static traffic: Runtime (s)', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-GIgBft6yszkBn6XVMLcE4zAAv6kSWb.png'],
  ['Dynamic traffic: Feasibility rate', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-srrm9ruilg8H7lLVFD3rvO8YzQTH4i.png'],
  ['Static traffic: Feasibility rate', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-iGcehsudfc4VCJxJBml5EmMRIKLdPR.png'],
  ['Static traffic: Objective evaluations', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-gOrBszjlMdHIrCUh6PBW0G6oDCd6eU.png'],
  ['Dynamic traffic: Runtime (s)', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-1lg6TIVXRAcgE0sA0VSK0tXLDVc5m1.png'],
  ['Traffic-induced objective degradation', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-MnbpsFBjmg5ltl2FcN1HCbK4QNLbzr.png'],
  ['Dynamic traffic: Objective evaluations', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-bcdBtljalSBd9JigJqI5qWQdA12myL.png'],
  ['Static traffic: Objective', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-t1Ko882T8rvgTmkPOgwPFWHA4eH5zx.png'],
  ['Dynamic traffic: Constraint violation', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-HVfcWqLaKC99rSo6kkI6y8QajJjNaC.png'],
  ['Dynamic traffic convergence (all raw runs)', 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-lVJmDqOjIDsMqtwpI9eMQLL1ai8gXb.png'],
] as const

export function TechnicalSectionPage({ page }: { page: PageKey }) {
  const data = pageData[page]
  const [figureIndex, setFigureIndex] = useState(0)
  const [figureTitle, figureUrl] = demonstrationFigures[figureIndex]
  return <main className="technical-page"><AppNavbar /><div className="technical-layout"><aside className="technical-sidebar"><div className="eyebrow"><Network size={14} /> VECTRA RESEARCH</div><h1>Network<br /><span>to result.</span></h1><p>Vehicle &amp; Traffic Route Optimization Architecture</p></aside><section className="technical-content"><div className="tech-hero"><div className="eyebrow">{data.eyebrow}</div><h2>{data.title}</h2><p>{data.intro}</p></div>
    {page === 'network-model' && <section className="tech-grid"><article className="tech-panel wide-panel"><div className="panel-topline"><Network size={18} /><div><div className="eyebrow">JAIPUR → AJMER</div><h3>Road graph on NH 48</h3></div></div><RouteMap algorithm="QPSO" traffic="Dynamic Traffic" /><p className="panel-copy">V is the set of network nodes and E is the set of directed road segments. Each customer has demand qᵢ, service time sᵢ, and time window [aᵢ, bᵢ]. Each vehicle k has capacity Qₖ.</p></article><article className="tech-panel compact-panel"><div className="eyebrow">MODEL ELEMENTS</div><ul className="signal-list"><li>G = (V, E)</li><li>Depot: node 0</li><li>Customer locations: V \ {'{0}'}</li><li>Vehicles: K</li><li>Capacity: Qₖ</li></ul></article></section>}
    {page === 'formulation' && <section className="tech-grid"><article className="tech-panel wide-panel"><div className="panel-topline"><BookOpen size={18} /><div><div className="eyebrow">DYNAMIC TRAFFIC MODEL</div><h3>Departure-time-dependent travel</h3></div></div><div className="formula-stack"><code>Cᵢⱼ(t) = clip(Bᵢⱼ + Aᵢⱼ sin(2πt/T + φᵢⱼ), 0, Cₘₐₓ)</code><code>τᵢⱼ(t) = τ⁰ᵢⱼ (1 + αCᵢⱼ(t))</code><code>F = Z + λQ VQ + λT VT + λR VR</code></div><p className="panel-copy">The route evaluator propagates arrival and departure times sequentially according to traffic conditions encountered along each route.</p></article><article className="tech-panel compact-panel"><div className="eyebrow">CONSTRAINTS</div><ul className="signal-list"><li>Customer visit exactly once</li><li>Vehicle flow conservation</li><li>Capacity: Σqᵢyᵢₖ ≤ Qₖ</li><li>Time windows: aᵢ ≤ tᵢₖ ≤ bᵢ</li><li>Depot origin and return</li></ul></article></section>}
    {page === 'algorithms' && <section className="algorithm-table">{algorithms.map(([name, idea], index) => <article className="algorithm-row" key={name}><span className="algorithm-rank rank-blue">0{index + 1}</span><div className="algorithm-name"><strong>{name}</strong><span>{idea}</span></div><div className="algorithm-tags"><span>Common evaluator</span><span>Static + dynamic</span></div></article>)}</section>}
    {page === 'platform' && <section className="tech-panel architecture-panel"><div className="pipeline">{[['Transportation-graph layer', Network], ['VRP instance representation', GitBranch], ['Static / Dynamic traffic models', Workflow], ['Shared objective evaluator', Check], ['Optimizer-specific implementations', BrainCircuit], ['Benchmark runner', Cpu], ['Result aggregation', Layers3], ['Matplotlib visualization', Code2]].map(([label, Icon], index) => <div key={String(label)}><Icon size={16} /><span>{String(index + 1).padStart(2, '0')}<br />{label as string}</span></div>)}</div></section>}
    {page === 'demonstration' && <section className="tech-panel demonstration-panel"><div className="panel-topline"><div><div className="eyebrow">DEMONSTRATION FIGURES</div><h3>{figureTitle}</h3></div><span className="figure-counter">{String(figureIndex + 1).padStart(2, '0')} / {String(demonstrationFigures.length).padStart(2, '0')}</span></div><div className="figure-frame"><img src={figureUrl} alt={figureTitle} /></div><div className="carousel-controls"><button type="button" onClick={() => setFigureIndex(index => (index - 1 + demonstrationFigures.length) % demonstrationFigures.length)}>Previous</button><span>{String(figureIndex + 1).padStart(2, '0')} / {String(demonstrationFigures.length).padStart(2, '0')}</span><button type="button" onClick={() => setFigureIndex(index => (index + 1) % demonstrationFigures.length)}>Next</button></div></section>}
  </section></div></main>
}
