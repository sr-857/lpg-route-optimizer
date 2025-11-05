from typing import List, Tuple
import math
import numpy as np

AVG_SPEED_KMPH = 30.0  # urban average


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def matrices(points: List[Tuple[float, float]], speed_kmph: float = AVG_SPEED_KMPH):
    n = len(points)
    dist = np.zeros((n, n), dtype=float)
    time_min = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            d = haversine_km(points[i][0], points[i][1], points[j][0], points[j][1])
            dist[i, j] = d
            time_min[i, j] = (d / speed_kmph) * 60.0
    return dist, time_min
