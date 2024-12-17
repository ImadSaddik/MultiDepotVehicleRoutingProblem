from tqdm import tqdm
from typing import List, Tuple
from psycopg2.extensions import cursor

from networkx import DiGraph
from networkx.algorithms.approximation import traveling_salesman_problem, greedy_tsp

from graph import get_connected_graph
from models import RouteSegment, OptimizeResponse, Node, ClusterData
from utils import (
    get_node_by_id,
    get_route_segments,
    get_employees_by_ids,
    calculate_total_distance,
    calculate_total_duration,
    make_shortest_path_with_unique_nodes
)


def get_optimized_routes(
    employees_to_bus_clusters: dict,
    company_node: Node,
    cursor: cursor,
) -> OptimizeResponse:
    optimized_routes = []

    for bus_id, employee_indices in tqdm(
        employees_to_bus_clusters.items(),
        total=len(employees_to_bus_clusters)
    ):
        if not employee_indices:
            continue

        bus_node = get_node_by_id(id_=bus_id, cursor=cursor)
        if not bus_node:
            continue

        assigned_employee_nodes = get_employees_by_ids(
            employee_indices, cursor=cursor)
        if not assigned_employee_nodes:
            continue

        sub_graph_nodes = [bus_node] + assigned_employee_nodes + [company_node]
        G = get_connected_graph(nodes=sub_graph_nodes, cursor=cursor)
        shortest_path = _find_shortest_path(G)
        shortest_path = make_shortest_path_with_unique_nodes(shortest_path)

        route_segments = _get_route_segments(
            nodes=sub_graph_nodes,
            shortest_path=shortest_path,
            cursor=cursor,
        )
        optimized_routes.append(ClusterData(
            bus_node=bus_node,
            employee_nodes=assigned_employee_nodes,
            company_node=company_node,
            total_distance=calculate_total_distance(route_segments),
            total_duration=calculate_total_duration(route_segments),
            route_segments=route_segments
        ))

    return OptimizeResponse(status="success", data=optimized_routes)


def _find_shortest_path(G: DiGraph) -> List[int]:
    node_indices = list(G.nodes)
    start_node_index = node_indices[0]  # Source (Bus node index)
    end_node_index = node_indices[-1]   # Sink (Company node index)

    intermediate_node_indices = node_indices[:-1]  # Bus node + Employee nodes
    tsp_path = traveling_salesman_problem(
        G.subgraph(intermediate_node_indices),
        cycle=False,
        method=greedy_tsp
    )

    # Rearrange the path to ensure it starts at the bus node
    if tsp_path[0] != start_node_index:
        bus_index = tsp_path.index(start_node_index)
        tsp_path = tsp_path[bus_index:] + tsp_path[:bus_index]

    return tsp_path + [end_node_index]


def _get_route_segments(
    nodes: List[Node],
    shortest_path: List[int],
    cursor: cursor
) -> List[RouteSegment]:
    route_segments = []
    for i in range(len(shortest_path) - 1):
        start_node_id, end_node_id = _get_start_end_node_ids(
            nodes=nodes,
            shortest_path=shortest_path[i:i+2]
        )
        route_segment = get_route_segments(
            source_node_id=start_node_id,
            destination_node_id=end_node_id,
            cursor=cursor
        )
        if not route_segment:
            continue

        route_segments.append(route_segment)

    return route_segments


def _get_start_end_node_ids(
    nodes: List[Node],
    shortest_path: List[int]
) -> Tuple[int, int]:
    start_node_index = shortest_path[0]
    end_node_index = shortest_path[-1]

    start_node = nodes[start_node_index]
    end_node = nodes[end_node_index]

    start_node_id = start_node.id
    end_node_id = end_node.id

    return start_node_id, end_node_id
