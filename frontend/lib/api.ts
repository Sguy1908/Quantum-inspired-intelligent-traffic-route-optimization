export type TrafficMode = 'dynamic' | 'static'

export type AlgorithmName = 'QPSO' | 'PSO' | 'GA' | 'ALNS' | 'Random Search'
export type TrafficState = 'free_flow' | 'moderate' | 'congested'

export type NetworkNode = {
  id: number
  x: number
  y: number
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
  congestion: number
  current_travel_time_min: number
  cost: number
}

export type Traversal = NetworkEdge & {
  start_time_min: number
  travel_time_min: number
  congestion: number
  vehicle: number
  cost: number
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
    runtime_ms: number
    objective_evaluations: number
  }
  traffic: {
    mode: TrafficMode
    timeline: Traversal[]
  }
  scenario: {
    seed: number
    nodes: number
    edges: number
    depot: number
    origin: number
    customers: number[]
    vehicles: number
    vehicle_capacity: number
    traffic_mode: TrafficMode
  }
  network: {
    nodes: NetworkNode[]
    edges: NetworkEdge[]
  }
  routes: number[][]
  expanded_routes: number[][]
  metrics: SimulationMetrics
  convergence_history: Array<{ evaluations: number; best_fitness: number }>
}

export type ComparisonResult = {
  results: Array<{
    name: AlgorithmName
    fitness: number
    feasible?: boolean
    distance_km: number
    travel_time_min: number
    total_cost: number
    runtime_ms: number
    objective_evaluations: number
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
  customers?: number
  max_iterations?: number
  max_evaluations?: number
  population?: number
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
  return request<SimulationResult>('/api/simulation/run', requestBody)
}

export function compareAlgorithms(requestBody: ComparisonRequest) {
  return request<ComparisonResult>('/api/simulation/compare', requestBody)
}
