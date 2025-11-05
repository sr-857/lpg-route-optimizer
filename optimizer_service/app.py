from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Tuple, Dict
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import math

app = FastAPI(title="LPG Optimizer Service")

# --- Distance helpers ---

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def matrices(points: List[Tuple[float, float]], speed_kmph: float = 30.0):
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

# --- Request/Response models ---

class Order(BaseModel):
    id: int
    lat: float
    lon: float
    demand: int = 1
    tw_start: int = 8*60
    tw_end: int = 18*60
    service_min: int = 10

class OptimizeRequest(BaseModel):
    depot: Tuple[float, float]
    orders: List[Order]
    num_vehicles: int = 3
    vehicle_capacity: int = 20
    speed_kmph: float = 30.0

class OptimizeResponse(BaseModel):
    routes: List[List[int]]
    total_distance_km: float
    total_time_min: float

# --- OR-Tools VRPTW ---

def solve_vrptw(num_vehicles: int,
                vehicle_capacity: int,
                demands: Dict[int, int],
                service_times_min: Dict[int, int],
                time_windows: Dict[int, Tuple[int, int]],
                travel_time_min: np.ndarray,
                dist_matrix_km: np.ndarray,
                depot_id: int = 0) -> List[List[int]]:
    n = travel_time_min.shape[0]
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot_id)
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(round(travel_time_min[from_node, to_node]))

    transit_cb_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

    routing.AddDimension(
        transit_cb_index,
        30,
        12*60,
        False,
        "Time",
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    for node in range(n):
        index = manager.NodeToIndex(node)
        service = int(service_times_min.get(node, 0))
        time_dimension.SlackVar(index).SetValue(service)
        if node in time_windows:
            start, end = time_windows[node]
            time_dimension.CumulVar(index).SetRange(start, end)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return int(demands.get(from_node, 0))

    demand_cb_idx = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_cb_idx,
        0,
        [vehicle_capacity] * num_vehicles,
        True,
        "Capacity",
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.FromSeconds(5)

    solution = routing.SolveWithParameters(search_parameters)
    routes: List[List[int]] = []
    if solution:
        for v in range(num_vehicles):
            idx = routing.Start(v)
            path = [manager.IndexToNode(idx)]
            while not routing.IsEnd(idx):
                idx = solution.Value(routing.NextVar(idx))
                path.append(manager.IndexToNode(idx))
            routes.append(path)
    else:
        routes = [[depot_id, depot_id] for _ in range(num_vehicles)]
    return routes

# --- Endpoint ---

@app.post("/optimize", response_model=OptimizeResponse)
def optimize(req: OptimizeRequest):
    points = [tuple(req.depot)] + [(o.lat, o.lon) for o in req.orders]
    dist_km, tmin = matrices(points, speed_kmph=req.speed_kmph)

    demands: Dict[int, int] = {o.id: o.demand for o in req.orders}
    service: Dict[int, int] = {o.id: o.service_min for o in req.orders}
    tw: Dict[int, Tuple[int, int]] = {o.id: (o.tw_start, o.tw_end) for o in req.orders}

    routes = solve_vrptw(
        num_vehicles=req.num_vehicles,
        vehicle_capacity=req.vehicle_capacity,
        demands=demands,
        service_times_min=service,
        time_windows=tw,
        travel_time_min=tmin,
        dist_matrix_km=dist_km,
        depot_id=0,
    )

    total_km = 0.0
    total_time = 0.0
    for r in routes:
        for a,b in zip(r[:-1], r[1:]):
            total_km += float(dist_km[a,b])
            total_time += float(tmin[a,b])
        for node in r[1:-1]:
            total_time += float(service.get(node, 0))

    return OptimizeResponse(routes=routes, total_distance_km=total_km, total_time_min=total_time)

# To run: uvicorn app:app --host 0.0.0.0 --port 8001
