from typing import List
from pydantic import BaseModel


class EmployeeData(BaseModel):
    id: int
    latitude: float
    longitude: float


class BusData(BaseModel):
    id: int
    latitude: float
    longitude: float


class CompanyData(BaseModel):
    latitude: float
    longitude: float


class OptimizeRequest(BaseModel):
    solver: str
    employees_data: List[EmployeeData]
    buses_data: List[BusData]
    company_data: CompanyData
    
    
class Location(BaseModel):
    latitude: float
    longitude: float


class RouteSegment(BaseModel):
    source: Location
    destination: Location
    distance: float
    duration: float
    coordinates: List[Location]
    
class OptimizeResponse(BaseModel):
    status: str
    routes: List[List[RouteSegment]]
