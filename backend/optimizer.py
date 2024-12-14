from tqdm import tqdm
from typing import List
from networkx import DiGraph
from networkx.algorithms.approximation import traveling_salesman_problem, greedy_tsp

from models import RouteSegment, OptimizeResponse, Location
from graph import get_connected_graph


def get_optimized_routes(
    employees_to_bus_clusters: dict,
    buses_data: List[tuple],
    employees_data: List[tuple],
    company_location: tuple,
    routes: dict,
) -> OptimizeResponse:
    optimized_routes = []

    for bus_idx, employee_indices in tqdm(
        employees_to_bus_clusters.items(),
        total=len(employees_to_bus_clusters)
    ):
        if not employee_indices:
            continue

        bus_location = buses_data[bus_idx]
        assigned_employees = [employees_data[i] for i in employee_indices]
        G = get_connected_graph(bus_location, assigned_employees, company_location, routes)
        shortest_path = _find_shortest_path(G)

        route_segments = _get_route_segments(
            shortest_path,
            bus_location,
            assigned_employees,
            company_location,
            routes
        )
        optimized_routes.append(route_segments)

    return OptimizeResponse(status="success", routes=optimized_routes)


def _find_shortest_path(G: DiGraph) -> List:
    nodes = list(G.nodes)
    start_node = nodes[0]  # Source (bus location)
    end_node = nodes[-1]   # Sink (company location)

    # Solve TSP for the intermediate nodes
    intermediate_nodes = nodes[1:-1]  # Employee nodes
    tsp_path = traveling_salesman_problem(
        G.subgraph(intermediate_nodes),
        cycle=False,
        method=greedy_tsp
    )

    # Include start and end
    full_path = [start_node] + tsp_path + [end_node]

    return full_path


def _get_route_segments(
    shortest_path: List,
    bus_location: tuple,
    employee_locations: List[tuple],
    company_location: tuple,
    routes: dict
) -> List[RouteSegment]:
    route_segments = []
    locations = [bus_location] + employee_locations + [company_location]

    for i in range(len(shortest_path) - 1):
        start_idx, end_idx = shortest_path[i], shortest_path[i + 1]
        start_loc = locations[start_idx]
        end_loc = locations[end_idx]

        route_key = tuple(sorted((tuple(start_loc), tuple(end_loc))))
        if route_key not in routes:
            continue

        route_info = routes[route_key]
        route_segment = RouteSegment(
            source=Location(latitude=start_loc[0], longitude=start_loc[1]),
            destination=Location(latitude=end_loc[0], longitude=end_loc[1]),
            distance=route_info['distance'],
            duration=route_info['duration'],
            coordinates=route_info['coordinates']
        )
        route_segments.append(route_segment)

    return route_segments
