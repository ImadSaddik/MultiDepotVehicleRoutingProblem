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


class OptimizeResponse(BaseModel):
    status: str
    routes: List[List[RouteSegment]]
