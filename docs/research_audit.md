# Pre-revamp simulator audit

## Implemented before the revamp

The repository represented a directed sparse road graph, generated random node coordinates and nearest-neighbour edges, and selected random customer nodes with demands, service times, and time windows. A random-key vector was sorted into a customer permutation then greedily capacity-split into depot-to-depot routes. QPSO, PSO, GA, and random search all used that decoder and a common penalty evaluator. Existing benchmark scripts ran repeated seeds and stored aggregate JSON plus figures.

The QPSO implementation used `mbest = mean(pbest)`, `p = phi*pbest + (1-phi)*gbest`, and `x_next = p ± beta*abs(mbest-x)*log(1/u)`, with a linear beta schedule and clipping to `[0,1]`.

## Issues found

* The stated dynamic model only mutated graph congestion between optimisation calls; an edge's travel time was constant within a route and `time_step` did not affect costs.
* Travel time was congestion-inflated and the objective also added raw congestion, an undocumented double-count unless deliberately modelled as a separate externality.
* The decoder could exceed the fleet limit and could emit an over-capacity route. Time windows and customer/flow rules were soft penalties, not enforced feasibility; duplicate visits were not penalised.
* Benchmark trials reused a mutable graph, so traffic conditions were not reliably paired across algorithms. Only iteration counts were recorded; objective evaluations were not.
* The former GA/PSO/random-search baselines shared the evaluator, but none was a strong route-neighbourhood VRP baseline. Some existing benchmark tests also passed an unsupported constructor argument.

These findings motivated the shared evaluator, immutable traffic scenarios, evaluation budgets, raw paired records, and ALNS baseline in this revamp. They are not retrospective claims about benchmark performance.
