export type TrafficMode = 'dynamic' | 'static'

export type AlgorithmName = 'QPSO' | 'PSO' | 'GA' | 'ALNS' | 'Random Search'
export type TrafficState = 'free_flow' | 'moderate' | 'congested'

export type NetworkNode = {
  id: number
  lat: number
  lng: number
  node_type: 'depot' | 'customer' | 'intersection'
}

export type NetworkEdge = {
  u: number
  v: number
  distance_km: number
  base_time_min: number
  traffic_state: TrafficState
}

export type Traversal = NetworkEdge & {
  start_time_min: number
  travel_time_min: number
}

export type SimulationMetrics = {
  distance_km: number
  travel_time_min: number
  average_speed_kmh: number
  total_cost: number
  nodes_visited: number
  fitness: number
  feasible: boolean
}

export type SimulationResult = {
  algorithm: {
    name: AlgorithmName
    iterations: number
    convergence_percent: number
  }
  traffic: {
    mode: TrafficMode
    timeline: Traversal[]
  }
  scenario: {
    seed: number
    nodes: number
    edges: number
    customers: number[]
  }
  network: {
    nodes: NetworkNode[]
    edges: NetworkEdge[]
  }
  routes: number[][]
  metrics: SimulationMetrics
}

export type ComparisonResult = {
  results: Array<{
    name: AlgorithmName
    fitness: number
    feasible?: boolean
  }>
  scenario?: SimulationResult['scenario']
  traffic_mode?: TrafficMode
}

export type SimulationRequest = {
  algorithm: AlgorithmName
  traffic_mode: TrafficMode
  nodes: number
  vehicles: number
  seed: number
}

export type ComparisonRequest = Omit<SimulationRequest, 'algorithm'>

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

async function request<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    const detail = await response.text().catch(() => '')
    throw new Error(detail || `API request failed with status ${response.status}.`)
  }

  return response.json() as Promise<T>
}

export function runSimulation(requestBody: SimulationRequest) {
  return request<SimulationResult>('/api/simulate', requestBody)
}

export function compareAlgorithms(requestBody: ComparisonRequest) {
  return request<ComparisonResult>('/api/compare', requestBody)
}
