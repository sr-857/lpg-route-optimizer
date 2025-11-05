from typing import List, Dict, Tuple
import numpy as np

# Very simple greedy baseline: assign customers to k vehicles in round-robin blocks
# with a nearest-neighbor sequence within each block. Ignores time windows/violations.


def greedy_baseline_routes(
    num_vehicles: int,
    demands: Dict[int, int],
    capacity: int,
    dist_matrix_km: np.ndarray,
    customer_ids: List[int],
    depot_id: int = 0,
) -> List[List[int]]:
    n_per_vehicle = max(1, len(customer_ids) // num_vehicles)
    routes: List[List[int]] = []
    remaining = customer_ids[:]

    for v in range(num_vehicles):
        if not remaining:
            routes.append([depot_id, depot_id])
            continue
        # Take a slice of customers, then route by NN
        block = remaining[: n_per_vehicle]
        remaining = remaining[n_per_vehicle:]
        # Respect capacity in a crude way: trim if needed
        cap = 0
        trimmed = []
        for cid in block:
            if cap + demands[cid] <= capacity:
                trimmed.append(cid)
                cap += demands[cid]
        seq = [depot_id]
        unvisited = trimmed[:]
        curr = depot_id
        while unvisited:
            nxt = min(unvisited, key=lambda x: dist_matrix_km[curr, x])
            seq.append(nxt)
            curr = nxt
            unvisited.remove(nxt)
        seq.append(depot_id)
        routes.append(seq)

    # If any remaining, append to last route (still baseline)
    for cid in remaining:
        routes[-1].insert(-1, cid)

    return routes
