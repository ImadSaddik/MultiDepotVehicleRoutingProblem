from typing import List
from psycopg2.extensions import cursor

from models import Node
from utils import get_route_segments

def assign_employees_to_buses(
    bus_nodes: List[Node],
    employee_nodes: List[Node],
    cursor: cursor,
    max_capacity: int = 18
) -> dict:
    bus_ids = [node.id for node in bus_nodes]
    employee_ids = [node.id for node in employee_nodes]

    assignments = {i: [] for i in bus_ids}
    unassigned_employees = set(employee_ids)

    for bus_node in bus_nodes:
        if not unassigned_employees:
            break

        distances = {}
        bus_node_id = bus_node.id
        for employee_node_id in unassigned_employees:
            route_segment = get_route_segments(
                source_node_id=bus_node_id,
                destination_node_id=employee_node_id,
                cursor=cursor
            )
            if not route_segment:
                distances[employee_node_id] = float('inf')
                continue
                
            distances[employee_node_id] = route_segment.distance

        sorted_employee_indices = sorted(distances, key=distances.get)

        for employee_node_id in sorted_employee_indices[:max_capacity]:
            if len(assignments[bus_node_id]) < max_capacity:
                assignments[bus_node_id].append(employee_node_id)

        assigned = set(assignments[bus_node_id])
        unassigned_employees -= assigned

    return assignments
