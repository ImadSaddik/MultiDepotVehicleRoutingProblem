import networkx as nx

from networkx import DiGraph
from typing import List
from psycopg2.extensions import cursor

from models import Node
from utils import get_route_segments

def get_connected_graph(
    nodes: List[Node],
    cursor: cursor
) -> DiGraph:
    G = nx.DiGraph()

    for i, source_node in enumerate(nodes):
        for j, destination_node in enumerate(nodes):
            if i == j:  # No self-loops
                continue

            source_node_id = source_node.id
            destination_node_id = destination_node.id
            route_segment = get_route_segments(
                source_node_id=source_node_id,
                destination_node_id=destination_node_id,
                cursor=cursor
            )
            if not route_segment:
                continue
            
            distance = route_segment.distance
            G.add_edge(i, j, weight=distance)

    return G
