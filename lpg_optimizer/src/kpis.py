from typing import List, Dict, Any
import numpy as np


def compute_kpis(
    routes: List[List[int]],
    dist_matrix_km: np.ndarray,
    service_times_min: Dict[int, int],
    travel_times_min: np.ndarray,
) -> Dict[str, Any]:
    total_km = 0.0
    total_travel_min = 0.0
    total_service_min = 0.0
    for route in routes:
        for a, b in zip(route[:-1], route[1:]):
            total_km += dist_matrix_km[a, b]
            total_travel_min += travel_times_min[a, b]
        for node in route[1:-1]:  # exclude depot at both ends
            total_service_min += service_times_min.get(node, 0)
    return {
        "total_distance_km": float(total_km),
        "total_travel_min": float(total_travel_min),
        "total_service_min": float(total_service_min),
        "total_time_min": float(total_travel_min + total_service_min),
    }
