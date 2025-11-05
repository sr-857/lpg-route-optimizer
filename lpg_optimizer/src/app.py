import json
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import streamlit as st

from dataset import generate_mock_dataset, to_dataframe
from distance import matrices
from baseline import greedy_baseline_routes
from optimize import solve_vrptw
from kpis import compute_kpis
from visualize import map_routes

st.set_page_config(page_title="LPG Route Optimizer", layout="wide")

st.title("LPG Smart Route Optimizer")

with st.sidebar:
    st.header("Scenario Settings")
    n_customers = st.slider("Customers", 10, 60, 25, 1)
    num_vehicles = st.slider("Trucks", 1, 8, 3, 1)
    vehicle_capacity = st.slider("Truck capacity (cylinders)", 5, 40, 20, 1)
    speed = st.slider("Avg speed (km/h)", 15, 60, 30, 1)
    seed = st.number_input("Random seed", value=42, step=1)
    st.caption("Adjust and click 'Run' below")
    run = st.button("Run Optimization", use_container_width=True)

if run:
    import random
    random.seed(int(seed))

    depot, customers = generate_mock_dataset(n_customers=n_customers)
    depot_df, cust_df = to_dataframe(depot, customers)

    # Build point list [depot + customers]
    points: List[Tuple[float, float]] = [(depot.lat, depot.lon)] + list(
        zip(cust_df.lat, cust_df.lon)
    )

    # Matrices
    dist_km, tmin = matrices(points, speed_kmph=float(speed))

    # Data dicts indexed by global node id
    demands: Dict[int, int] = {int(r.id): int(r.demand) for _, r in cust_df.iterrows()}
    service_times: Dict[int, int] = {int(r.id): int(r.service_min) for _, r in cust_df.iterrows()}
    tw: Dict[int, Tuple[int, int]] = {
        int(r.id): (int(r.tw_start_min), int(r.tw_end_min)) for _, r in cust_df.iterrows()
    }
    names: Dict[int, str] = {0: depot.name}
    for _, r in cust_df.iterrows():
        names[int(r.id)] = f"{r.name} (d={int(r.demand)})"

    customer_ids = [int(i) for i in cust_df.id.tolist()]

    # Baseline
    baseline_routes = greedy_baseline_routes(
        num_vehicles=num_vehicles,
        demands=demands,
        capacity=vehicle_capacity,
        dist_matrix_km=dist_km,
        customer_ids=customer_ids,
        depot_id=0,
    )

    # Optimized
    opt_routes = solve_vrptw(
        num_vehicles=num_vehicles,
        vehicle_capacity=vehicle_capacity,
        demands=demands,
        service_times_min=service_times,
        time_windows=tw,
        travel_time_min=tmin,
        dist_matrix_km=dist_km,
        depot_id=0,
    )

    # KPIs
    base_kpis = compute_kpis(baseline_routes, dist_km, service_times, tmin)
    opt_kpis = compute_kpis(opt_routes, dist_km, service_times, tmin)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Before (Baseline)")
        st.metric("Distance (km)", f"{base_kpis['total_distance_km']:.1f}")
        st.metric("Total time (min)", f"{base_kpis['total_time_min']:.0f}")
    with col2:
        st.subheader("After (Optimized)")
        st.metric("Distance (km)", f"{opt_kpis['total_distance_km']:.1f}")
        st.metric("Total time (min)", f"{opt_kpis['total_time_min']:.0f}")

    # Reduction
    if base_kpis["total_distance_km"] > 0:
        dist_red = 100.0 * (base_kpis["total_distance_km"] - opt_kpis["total_distance_km"]) / base_kpis["total_distance_km"]
    else:
        dist_red = 0.0
    if base_kpis["total_time_min"] > 0:
        time_red = 100.0 * (base_kpis["total_time_min"] - opt_kpis["total_time_min"]) / base_kpis["total_time_min"]
    else:
        time_red = 0.0

    st.success(
        f"Estimated reduction — Distance: {dist_red:.1f}% | Total time: {time_red:.1f}%"
    )

    # Maps (embed folium)
    from visualize import map_routes
    import streamlit.components.v1 as components

    base_map = map_routes(points, baseline_routes, names, title="Baseline Routes")
    opt_map = map_routes(points, opt_routes, names, title="Optimized Routes")

    with st.expander("Before (Baseline) Map", expanded=True):
        components.html(base_map._repr_html_(), height=520)
    with st.expander("After (Optimized) Map", expanded=True):
        components.html(opt_map._repr_html_(), height=520)

    # Optional: export simple slide image
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(["Before", "After"], [base_kpis["total_time_min"], opt_kpis["total_time_min"]], color=["#d62728", "#2ca02c"])
    ax.set_ylabel("Total time (min)")
    ax.set_title("Route Optimization Impact")
    st.pyplot(fig)

    # Offer JSON export
    st.download_button(
        label="Download KPIs JSON",
        data=json.dumps({"baseline": base_kpis, "optimized": opt_kpis}, indent=2),
        file_name="kpis.json",
        mime="application/json",
    )
else:
    st.info("Configure parameters in the sidebar and click Run Optimization.")
