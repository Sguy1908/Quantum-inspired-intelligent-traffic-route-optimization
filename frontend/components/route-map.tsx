'use client'

import 'leaflet/dist/leaflet.css'
import { useMemo } from 'react'
import { CircleMarker, MapContainer, Polyline, TileLayer, Tooltip, useMap } from 'react-leaflet'
import type { LatLngExpression } from 'leaflet'

type Traffic = 'Dynamic Traffic' | 'Static Traffic'

type RouteMapProps = { algorithm: string; traffic: Traffic }

const paths: Record<string, LatLngExpression[]> = {
  QPSO: [[37.792, -122.442], [37.786, -122.431], [37.779, -122.424], [37.771, -122.418], [37.764, -122.409], [37.758, -122.401], [37.751, -122.394]],
  GA: [[37.792, -122.442], [37.787, -122.435], [37.781, -122.427], [37.775, -122.421], [37.765, -122.416], [37.758, -122.406], [37.751, -122.394]],
  ALNS: [[37.792, -122.442], [37.799, -122.433], [37.793, -122.421], [37.784, -122.416], [37.775, -122.411], [37.765, -122.405], [37.751, -122.394]],
  PSO: [[37.792, -122.442], [37.798, -122.438], [37.801, -122.425], [37.789, -122.415], [37.778, -122.405], [37.764, -122.399], [37.751, -122.394]],
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
      <MapContainer center={[37.775, -122.419]} zoom={13} zoomControl={true} scrollWheelZoom={false} className="real-map">
        <TileLayer attribution='&copy; OpenStreetMap contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Recenter points={points} />
        <Polyline positions={points} pathOptions={{ color: '#7d91a6', weight: 7, opacity: 0.34, dashArray: '7 9' }} />
        <Polyline positions={points} pathOptions={{ color: dynamic ? '#337cff' : '#8aa2b5', weight: 5, opacity: dynamic ? 0.98 : 0.65 }} />
        {trafficPoints.map((point, index) => <CircleMarker key={`${point[0]}-${point[1]}`} center={point} radius={index % 3 === 1 && dynamic ? 7 : 5} pathOptions={{ color: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78', fillColor: index % 3 === 1 && dynamic ? '#e45b4d' : '#6bdb78', fillOpacity: 0.95, weight: 2 }}><Tooltip>{dynamic ? `Traffic checkpoint ${index + 1}` : `Waypoint ${index + 1}`}</Tooltip></CircleMarker>)}
        <CircleMarker center={points[0]} radius={10} pathOptions={{ color: '#61dd73', fillColor: '#61dd73', fillOpacity: 0.9, weight: 3 }}><Tooltip permanent direction="right">START</Tooltip></CircleMarker>
        <CircleMarker center={points[points.length - 1]} radius={10} pathOptions={{ color: '#f0644f', fillColor: '#f0644f', fillOpacity: 0.9, weight: 3 }}><Tooltip permanent direction="left">END</Tooltip></CircleMarker>
      </MapContainer>
      <div className="map-status"><span className={`status-dot ${dynamic ? '' : 'static-dot'}`} />{dynamic ? 'LIVE TRAFFIC' : 'STATIC TRAFFIC'} <small>• {algorithm} route engine</small></div>
      <div className="map-legend"><span><b className="legend-blue" />Optimized route</span><span><b className="legend-green" />Free flow</span><span><b className="legend-red" />Congested</span></div>
    </div>
  )
}
