'use client'

import 'leaflet/dist/leaflet.css'
import { useEffect, useMemo, useState } from 'react'
import { CircleMarker, MapContainer, Polyline, TileLayer, Tooltip, useMap } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'
import type { NetworkEdge, SimulationResult, Traversal } from '@/lib/api'

type RouteMapProps = { result: SimulationResult | null }

const trafficColours = { free_flow: '#6bdb78', moderate: '#f7a11b', congested: '#e45b4d' }

function Recenter({ points }: { points: LatLngExpression[] }) {
  const map = useMap()
  useEffect(() => {
    if (points.length > 1) map.fitBounds(points as [number, number][], { padding: [28, 28] })
  }, [map, points])
  return null
}

function edgeKey(edge: Pick<NetworkEdge | Traversal, 'u' | 'v'>) { return `${edge.u}:${edge.v}` }

export function RouteMap({ result }: RouteMapProps) {
  const [timelineIndex, setTimelineIndex] = useState(0)
  const dynamic = result?.traffic.mode === 'dynamic'
  const nodesById = useMemo(() => new Map(result?.network.nodes.map(node => [node.id, node]) ?? []), [result])
  const routePoints = useMemo(() => (result?.routes ?? []).map(route => route.map(id => {
    const node = nodesById.get(id)
    return node ? [node.lat, node.lng] as LatLngExpression : null
  }).filter((point): point is LatLngExpression => point !== null)), [result, nodesById])
  const allPoints = routePoints.flat()
  const timeline = result?.traffic.timeline ?? []
  const activeTraversal = timeline[timelineIndex]

  useEffect(() => { setTimelineIndex(0) }, [result])
  useEffect(() => {
    if (!dynamic || timeline.length < 2) return
    const interval = window.setInterval(() => setTimelineIndex(current => (current + 1) % timeline.length), 900)
    return () => window.clearInterval(interval)
  }, [dynamic, timeline.length])

  if (!result) return <div className="real-map-shell map-empty"><div><strong>Ready to optimise</strong><span>Select an algorithm and run a seeded traffic scenario to render its actual network and route.</span></div></div>

  const visibleEdges = result.network.edges.filter(edge => edge.u < edge.v)
  const routeEdgeKeys = new Set(timeline.map(edgeKey))
  const center: LatLngExpression = allPoints[0] ?? [26.65, 75.60]
  const pointFor = (id: number) => {
    const node = nodesById.get(id)
    return node ? [node.lat, node.lng] as LatLngExpression : null
  }

  return (
    <div className="real-map-shell" aria-label={`${result.algorithm.name} ${result.traffic.mode} route map`}>
      <MapContainer center={center} zoom={11} zoomControl scrollWheelZoom={false} className="real-map">
        <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Recenter points={allPoints} />
        {visibleEdges.map(edge => {
          const first = pointFor(edge.u); const second = pointFor(edge.v)
          if (!first || !second) return null
          const isRoute = routeEdgeKeys.has(edgeKey(edge)) || routeEdgeKeys.has(`${edge.v}:${edge.u}`)
          return <Polyline key={`network-${edge.u}-${edge.v}`} positions={[first, second]} pathOptions={{ color: trafficColours[edge.traffic_state], weight: isRoute ? 3 : 1.2, opacity: isRoute ? 0.72 : 0.27 }} />
        })}
        {routePoints.map((points, index) => points.length > 1 && <Polyline key={`route-outline-${index}`} positions={points} pathOptions={{ color: '#07101f', weight: 7, opacity: 0.72 }} />)}
        {routePoints.map((points, index) => points.length > 1 && <Polyline key={`route-${index}`} positions={points} pathOptions={{ color: '#337cff', weight: 4.5, opacity: 0.98 }} />)}
        {result.network.nodes.filter(node => node.node_type !== 'intersection').map(node => {
          const depot = node.node_type === 'depot'
          return <CircleMarker key={node.id} center={[node.lat, node.lng]} radius={depot ? 9 : 5} pathOptions={{ color: depot ? '#61dd73' : '#b9d2f7', fillColor: depot ? '#61dd73' : '#397eff', fillOpacity: 0.95, weight: 2 }}><Tooltip>{depot ? 'DEPOT / START & RETURN' : `Customer ${node.id}`}</Tooltip></CircleMarker>
        })}
        {activeTraversal && (() => {
          const from = pointFor(activeTraversal.u); const to = pointFor(activeTraversal.v)
          return from && to ? <Polyline positions={[from, to]} pathOptions={{ color: trafficColours[activeTraversal.traffic_state], weight: 7, opacity: 0.95 }}><Tooltip sticky>{`${activeTraversal.traffic_state.replace('_', ' ')} at ${activeTraversal.start_time_min.toFixed(1)} min`}</Tooltip></Polyline> : null
        })()}
      </MapContainer>
      <div className="map-status"><span className={`status-dot ${dynamic ? '' : 'static-dot'}`} />{dynamic ? 'DYNAMIC TRAFFIC' : 'STATIC TRAFFIC'} <small>• seed {result.scenario.seed} • {result.algorithm.name} route execution {dynamic && timeline.length ? `• edge ${timelineIndex + 1}/${timeline.length}` : ''}</small></div>
      <div className="map-legend"><span><b className="legend-blue" />Optimized route</span><span><b className="legend-green" />Free flow</span><span><b className="legend-orange" />Moderate</span><span><b className="legend-red" />Congested</span></div>
    </div>
  )
}
