from typing import List, Dict, Tuple
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# Build VRP with Time Windows and Capacity.


def solve_vrptw(
    num_vehicles: int,
    vehicle_capacity: int,
    demands: Dict[int, int],
    service_times_min: Dict[int, int],
    time_windows: Dict[int, Tuple[int, int]],
    travel_time_min: np.ndarray,
    dist_matrix_km: np.ndarray,
    depot_id: int = 0,
) -> List[List[int]]:
    n = travel_time_min.shape[0]
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot_id)
    routing = pywrapcp.RoutingModel(manager)

    # Transit callback for time
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(round(travel_time_min[from_node, to_node]))

    transit_cb_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_cb_index)

    # Time dimension (includes service time)
    routing.AddDimension(
        transit_cb_index,
        30,  # slack max
        12 * 60,  # vehicle time horizon (minutes)
        False,
        "Time",
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    # Add service times and TWs
    for node in range(n):
        index = manager.NodeToIndex(node)
        service = int(service_times_min.get(node, 0))
        time_dimension.SlackVar(index).SetValue(service)
        if node in time_windows:
            start, end = time_windows[node]
            time_dimension.CumulVar(index).SetRange(start, end)

    # Capacity dimension
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

    # Search
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
        # Return empty routes if infeasible
        routes = [[depot_id, depot_id] for _ in range(num_vehicles)]
    return routes
