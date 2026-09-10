'use client'

import 'leaflet/dist/leaflet.css'
import { useMemo } from 'react'
import { CircleMarker, MapContainer, Polyline, TileLayer, Tooltip, useMap } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'

type Traffic = 'Dynamic Traffic' | 'Static Traffic'

type RouteMapProps = { algorithm: string; traffic: Traffic }

const paths: Record<string, LatLngExpression[]> = {
  QPSO: [[26.9124, 75.7873], [26.8582, 75.7115], [26.7967, 75.6389], [26.7354, 75.5657], [26.6718, 75.4858], [26.6031, 75.3788], [26.5265, 75.2314], [26.4934, 75.0648], [26.4499, 74.6399]],
  GA: [[26.9124, 75.7873], [26.8712, 75.7205], [26.8151, 75.6548], [26.7552, 75.5841], [26.6994, 75.5012], [26.6252, 75.3893], [26.5483, 75.2438], [26.5047, 75.0716], [26.4499, 74.6399]],
  ALNS: [[26.9124, 75.7873], [26.8814, 75.7429], [26.8274, 75.6814], [26.7688, 75.6118], [26.7063, 75.5352], [26.6461, 75.4305], [26.5628, 75.2791], [26.4499, 74.6399]],
  PSO: [[26.9124, 75.7873], [26.8942, 75.7351], [26.8425, 75.6678], [26.7797, 75.5945], [26.7182, 75.5149], [26.6574, 75.4056], [26.5757, 75.2582], [26.4499, 74.6399]],
}

function Recenter({ points }: { points: LatLngExpression[] }) {
  const map = useMap()
  useMemo(() => {
    map.fitBounds(points as [number, number][], { padding: [28, 28] })
  }, [map, points])
  return null
}

export function RouteMap({ algorithm, traffic }: RouteMapProps) {
  const points = paths[algorithm] ?? paths.QPSO
  const dynamic = traffic === 'Dynamic Traffic'
  const trafficPoints = points.slice(1, -1)

  return (
    <div className="real-map-shell" aria-label={`${algorithm} ${traffic} route map`}>
      <MapContainer center={[26.681, 75.215]} zoom={9} zoomControl={true} scrollWheelZoom={false} className="real-map">
        <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Recenter points={points} />
        <Polyline positions={points} pathOptions={{ color: '#7d91a6', weight: 7, opacity: 0.34, dashArray: '7 9' }} />
        <Polyline positions={points} pathOptions={{ color: dynamic ? '#337cff' : '#8aa2b5', weight: 5, opacity: dynamic ? 0.98 : 0.65 }} />
        {trafficPoints.map((point, index) => <CircleMarker key={`${point[0]}-${point[1]}`} center={point} radius={index % 3 === 1 && dynamic ? 7 : 5} pathOptions={{ color: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78', fillColor: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78', fillOpacity: 0.95, weight: 2 }}><Tooltip>{dynamic ? `Traffic checkpoint ${index + 1}` : `Waypoint ${index + 1}`}</Tooltip></CircleMarker>)}
        <CircleMarker center={points[0]} radius={10} pathOptions={{ color: '#61dd73', fillColor: '#61dd73', fillOpacity: 0.9, weight: 3 }}><Tooltip permanent direction="right">START</Tooltip></CircleMarker>
        <CircleMarker center={points[points.length - 1]} radius={10} pathOptions={{ color: '#f0644f', fillColor: '#f0644f', fillOpacity: 0.9, weight: 3 }}><Tooltip permanent direction="left">END</Tooltip></CircleMarker>
      </MapContainer>
      <div className="map-status"><span className={`status-dot ${dynamic ? '' : 'static-dot'}`} />{dynamic ? 'LIVE TRAFFIC' : 'STATIC TRAFFIC'} <small>• Jaipur → Ajmer NH 48 • {algorithm} route engine</small></div>
      <div className="map-legend"><span><b className="legend-blue" />Optimized route</span><span><b className="legend-green" />Free flow</span><span><b className="legend-red" />Congested</span></div>
    </div>
  )
}
