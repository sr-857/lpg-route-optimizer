from typing import List, Tuple, Dict
import folium

COLORS = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#a65628",
    "#f781bf",
    "#999999",
]


def map_routes(
    points: List[Tuple[float, float]],
    routes: List[List[int]],
    names: Dict[int, str],
    title: str,
) -> folium.Map:
    center = points[0]
    m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")
    folium.Marker(
        location=center,
        popup=f"Depot: {names[0]}",
        icon=folium.Icon(color="black", icon="home"),
    ).add_to(m)

    for ridx, route in enumerate(routes):
        color = COLORS[ridx % len(COLORS)]
        coords = [points[i] for i in route]
        folium.PolyLine(coords, color=color, weight=4, opacity=0.8).add_to(m)
        for node in route[1:-1]:
            folium.CircleMarker(
                location=points[node],
                radius=4,
                color=color,
                fill=True,
                fill_color=color,
                popup=names.get(node, str(node)),
            ).add_to(m)

    folium.map.LayerControl().add_to(m)

    title_html = f"""
         <h3 align="center" style="font-size:16px"><b>{title}</b></h3>
         """
    m.get_root().html.add_child(folium.Element(title_html))
    return m
