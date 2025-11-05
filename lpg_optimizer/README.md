# LPG Smart Route Optimizer

This demo generates a mock LPG delivery scenario and optimizes routes using Google OR-Tools (VRP with time windows and vehicle capacity). It visualizes baseline (naive) vs optimized routes on a map and shows KPIs.

## Quick start

1) Create a Python venv (optional) and install deps:

```
pip install -r lpg_optimizer/requirements.txt
```

2) Run the dashboard:

```
streamlit run lpg_optimizer/src/app.py
```

This will:
- Generate a mock dataset (one depot, multiple customers with time windows and demands)
- Compute a naive baseline routing
- Compute an optimized routing with OR-Tools
- Show KPIs and maps (Before vs After)

3) CLI pipeline (optional):

```
python lpg_optimizer/src/run_pipeline.py
```

Artifacts will be saved under `lpg_optimizer/outputs`.

## Notes
- Speed is approximated (30 km/h) with Haversine distances.
- Time windows and service durations are synthetic but realistic.
- Adjust constants in `dataset.py` if needed.
