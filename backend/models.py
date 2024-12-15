from typing import List
from pydantic import BaseModel


class Node(BaseModel):
    id: int
    latitude: float
    longitude: float
    type_: str


class Point(BaseModel):
    latitude: float
    longitude: float


class RouteSegment(BaseModel):
    source_node_id: int
    destination_node_id: int
    distance: float
    duration: float
    coordinates: List[Point]


class ClusterData(BaseModel):
    bus_node: Node
    employee_nodes: List[Node]
    company_node: Node
    total_distance: float
    total_duration: float
    route_segments: List[RouteSegment]


class OptimizeResponse(BaseModel):
    status: str
    data: List[ClusterData]
