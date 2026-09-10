'use client'

import 'leaflet/dist/leaflet.css'
import { useEffect, useMemo } from 'react'
import { CircleMarker, MapContainer, Polyline, TileLayer, Tooltip, useMap } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'
import type { SimulationResult } from '@/lib/api'

type Traffic = 'Dynamic Traffic' | 'Static Traffic'
type RouteMapProps = { algorithm: string; traffic: Traffic; result?: SimulationResult | null }

const trafficColors = { free_flow: '#6bdb78', moderate: '#f6b73c', congested: '#e45b4d' } as const

function Recenter({ points }: { points: LatLngExpression[] }) {
  const map = useMap()
  useEffect(() => {
    if (points.length > 1) map.fitBounds(points as [number, number][], { padding: [28, 28] })
  }, [map, points])
  return null
}

export function RouteMap({ algorithm, traffic, result }: RouteMapProps) {
  const data = useMemo(() => {
    if (!result) return null
    const nodes = new Map(result.network.nodes.map(node => [node.id, node]))
    const timelineByEdge = new Map(result.traffic.timeline.map(edge => [`${edge.u}-${edge.v}`, edge]))
    const routeLines = result.expanded_routes
      .map(route => route.map(nodeId => nodes.get(nodeId)).filter((node): node is NonNullable<typeof node> => Boolean(node)).map(node => [node.lat, node.lng] as [number, number]))
      .filter(route => route.length > 1)
    const points = result.network.nodes.map(node => [node.lat, node.lng] as [number, number])
    return { nodes, timelineByEdge, routeLines, points }
  }, [result])

  if (!result || !data) return <div className="real-map-shell map-loading" aria-live="polite">Run a scenario to display the generated network and optimized route.</div>

  const dynamic = traffic === 'Dynamic Traffic'
  return (
    <div className="real-map-shell" aria-label={`${algorithm} ${traffic} route map`}>
      <MapContainer center={data.points[0]} zoom={11} zoomControl scrollWheelZoom={false} className="real-map">
        <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Recenter points={data.points} />
        {result.network.edges.map(edge => {
          const source = data.nodes.get(edge.u)
          const target = data.nodes.get(edge.v)
          if (!source || !target) return null
          const observed = data.timelineByEdge.get(`${edge.u}-${edge.v}`)
          const state = observed?.traffic_state ?? edge.traffic_state
          return <Polyline key={`${edge.u}-${edge.v}`} positions={[[source.lat, source.lng], [target.lat, target.lng]]} pathOptions={{ color: trafficColors[state], weight: 2, opacity: 0.38 }} />
        })}
        {data.routeLines.map((route, index) => <Polyline key={`route-${index}`} positions={route} pathOptions={{ color: '#337cff', weight: 5, opacity: 0.96 }} />)}
        {result.network.nodes.map(node => {
          const isDepot = node.id === result.scenario.depot
          const isCustomer = result.scenario.customers.includes(node.id)
          const color = isDepot ? '#61dd73' : isCustomer ? '#f6b73c' : '#7d91a6'
          const label = isDepot ? 'DEPOT' : isCustomer ? `CUSTOMER ${node.id}` : `NODE ${node.id}`
          return <CircleMarker key={node.id} center={[node.lat, node.lng]} radius={isDepot ? 9 : isCustomer ? 6 : 3} pathOptions={{ color, fillColor: color, fillOpacity: 0.9, weight: 1 }}><Tooltip>{label}</Tooltip></CircleMarker>
        })}
      </MapContainer>
      <div className="map-status"><span className={`status-dot ${dynamic ? '' : 'static-dot'}`} />{dynamic ? 'DYNAMIC TRAFFIC' : 'STATIC TRAFFIC'} <small>• seeded synthetic network • {algorithm}</small></div>
      <div className="map-legend"><span><b className="legend-blue" />Optimized route</span><span><b className="legend-green" />Free flow</span><span><b className="legend-amber" />Moderate</span><span><b className="legend-red" />Congested</span></div>
    </div>
  )
}
