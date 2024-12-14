import networkx as nx

from typing import List
from networkx import DiGraph

def get_connected_graph(
    bus_location: tuple,
    employee_locations: List[tuple],
    company_location: tuple,
    routes: List[dict]
) -> DiGraph:
    locations = [bus_location] + employee_locations + [company_location]
    G = nx.DiGraph()

    for i, loc1 in enumerate(locations):
        for j, loc2 in enumerate(locations):
            if i == j:  # No self-loops
                continue

            key = tuple(sorted((tuple(loc1), tuple(loc2))))
            if key not in routes:
                continue

            route = routes[key]
            distance = route['distance']
            G.add_edge(i, j, weight=distance)

    return G
