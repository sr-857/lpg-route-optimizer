import random
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd

# Deterministic seed for reproducibility
random.seed(42)

@dataclass
class Depot:
    id: int
    name: str
    lat: float
    lon: float

@dataclass
class Customer:
    id: int
    name: str
    lat: float
    lon: float
    demand: int  # cylinders
    tw_start_min: int  # minutes from day start
    tw_end_min: int
    service_min: int


def generate_mock_dataset(
    n_customers: int = 25,
    city_center: Tuple[float, float] = (18.5204, 73.8567),  # Pune, IN
    radius_km: float = 12.0,
    day_start_min: int = 8 * 60,
    day_end_min: int = 18 * 60,
) -> Tuple[Depot, List[Customer]]:
    """Generate one depot at city center and customers around it within radius_km."""
    depot = Depot(id=0, name="Main Depot", lat=city_center[0], lon=city_center[1])

    customers: List[Customer] = []

    def jitter() -> Tuple[float, float]:
        # Convert ~km to lat/lon degrees (roughly: 1 deg lat ~ 111 km, lon scales by cos(lat))
        lat_km = radius_km
        lon_km = radius_km * max(0.2, abs(__import__('math').cos(__import__('math').radians(city_center[0]))))
        dlat = (random.uniform(-lat_km, lat_km)) / 111.0
        dlon = (random.uniform(-lon_km, lon_km)) / 111.0
        return city_center[0] + dlat, city_center[1] + dlon

    for i in range(1, n_customers + 1):
        lat, lon = jitter()
        demand = random.choice([1, 1, 2])  # most orders 1-2 cylinders
        # Split day into windows with some slack
        start = random.randint(day_start_min, day_end_min - 120)
        end = start + random.choice([90, 120, 180])
        end = min(end, day_end_min)
        service = random.choice([10, 15, 20])
        customers.append(
            Customer(
                id=i,
                name=f"C{i:02d}",
                lat=lat,
                lon=lon,
                demand=demand,
                tw_start_min=start,
                tw_end_min=end,
                service_min=service,
            )
        )

    return depot, customers


def to_dataframe(depot: Depot, customers: List[Customer]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    depot_df = pd.DataFrame([
        {"id": depot.id, "name": depot.name, "lat": depot.lat, "lon": depot.lon}
    ])
    cust_df = pd.DataFrame([
        {
            "id": c.id,
            "name": c.name,
            "lat": c.lat,
            "lon": c.lon,
            "demand": c.demand,
            "tw_start_min": c.tw_start_min,
            "tw_end_min": c.tw_end_min,
            "service_min": c.service_min,
        }
        for c in customers
    ])
    return depot_df, cust_df
