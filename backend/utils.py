from typing import List

from typing import Optional
from psycopg2.extensions import cursor

from models import RouteSegment, Point, Node


def get_route_segments(
    source_node_id: int,
    destination_node_id: int,
    cursor: cursor
) -> Optional[RouteSegment]:
    cursor.execute("""
    SELECT * FROM route_mapping 
    WHERE (source_node_id = %s AND destination_node_id = %s)
    OR (source_node_id = %s AND destination_node_id = %s)
    """, (source_node_id, destination_node_id, destination_node_id, source_node_id))

    data = cursor.fetchall()
    if not data:
        return None

    row = data[0]
    return RouteSegment(
        source_node_id=row[0],
        destination_node_id=row[1],
        distance=row[2],
        duration=row[3],
        coordinates=[
            Point(
                latitude=latitudeLongitude[0],
                longitude=latitudeLongitude[1]
            )
            for latitudeLongitude in row[4]
        ]
    )


def get_node_by_id(id_: int, cursor: cursor) -> Optional[Node]:
    cursor.execute("""
    SELECT * FROM nodes WHERE id = %s AND type = 'bus'
    """, (id_,))

    data = cursor.fetchall()
    if not data:
        return None

    row = data[0]
    return Node(id=row[0], latitude=row[1], longitude=row[2], type_=row[3])


def get_employees_by_ids(employee_ids: List[int], cursor: cursor) -> List[Node]:
    cursor.execute("""
    SELECT * FROM nodes WHERE id = ANY(%s) AND type = 'employee'
    """, (employee_ids,))

    data = cursor.fetchall()
    return [
        Node(id=row[0], latitude=row[1], longitude=row[2], type_=row[3])
        for row in data
    ]


def make_shortest_path_with_unique_nodes(shortest_path: List[int]) -> List[int]:
    already_assigned = set()

    shortest_path_with_unique_nodes = []
    for node in shortest_path:
        if node not in already_assigned:
            shortest_path_with_unique_nodes.append(node)
            already_assigned.add(node)

    return shortest_path_with_unique_nodes


def calculate_total_distance(route_segments: List[RouteSegment]) -> float:
    return sum([route_segment.distance for route_segment in route_segments])


def calculate_total_duration(route_segments: List[RouteSegment]) -> float:
    return sum([route_segment.duration for route_segment in route_segments])
