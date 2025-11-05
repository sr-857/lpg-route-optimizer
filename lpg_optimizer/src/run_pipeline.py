import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from dataset import generate_mock_dataset, to_dataframe
from distance import matrices
from baseline import greedy_baseline_routes
from optimize import solve_vrptw
from kpis import compute_kpis
from visualize import map_routes

OUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    depot, customers = generate_mock_dataset(n_customers=25)
    depot_df, cust_df = to_dataframe(depot, customers)

    points = [(depot.lat, depot.lon)] + list(zip(cust_df.lat, cust_df.lon))
    dist_km, tmin = matrices(points)

    demands: Dict[int, int] = {int(r.id): int(r.demand) for _, r in cust_df.iterrows()}
    service_times: Dict[int, int] = {int(r.id): int(r.service_min) for _, r in cust_df.iterrows()}
    tw: Dict[int, Tuple[int, int]] = {
        int(r.id): (int(r.tw_start_min), int(r.tw_end_min)) for _, r in cust_df.iterrows()
    }
    names: Dict[int, str] = {0: depot.name}
    for _, r in cust_df.iterrows():
        names[int(r.id)] = f"{r.name} (d={int(r.demand)})"

    num_vehicles = 3
    capacity = 20

    baseline_routes = greedy_baseline_routes(
        num_vehicles=num_vehicles,
        demands=demands,
        capacity=capacity,
        dist_matrix_km=dist_km,
        customer_ids=list(cust_df.id),
        depot_id=0,
    )

    opt_routes = solve_vrptw(
        num_vehicles=num_vehicles,
        vehicle_capacity=capacity,
        demands=demands,
        service_times_min=service_times,
        time_windows=tw,
        travel_time_min=tmin,
        dist_matrix_km=dist_km,
        depot_id=0,
    )

    base_kpis = compute_kpis(baseline_routes, dist_km, service_times, tmin)
    opt_kpis = compute_kpis(opt_routes, dist_km, service_times, tmin)

    # Save KPIs
    with open(OUT_DIR / "kpis.json", "w") as f:
        json.dump({"baseline": base_kpis, "optimized": opt_kpis}, f, indent=2)

    # Save maps
    base_map = map_routes(points, baseline_routes, names, title="Baseline Routes")
    base_map.save(str(OUT_DIR / "baseline_map.html"))
    opt_map = map_routes(points, opt_routes, names, title="Optimized Routes")
    opt_map.save(str(OUT_DIR / "optimized_map.html"))

    # Simple bar chart slide
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(["Before", "After"], [base_kpis["total_time_min"], opt_kpis["total_time_min"]], color=["#d62728", "#2ca02c"])
    ax.set_ylabel("Total time (min)")
    ax.set_title("Route Optimization Impact")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "impact_slide.png", dpi=160)

    print("Saved outputs to:", OUT_DIR)


if __name__ == "__main__":
    main()
