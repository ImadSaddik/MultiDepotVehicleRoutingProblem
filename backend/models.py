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
    
    
class RouteSegment(BaseModel):
    source: tuple
    destination: tuple
    distance: float
    duration: float
    coordinates: List[tuple]
    
class OptimizeResponse(BaseModel):
    status: str
    routes: List[List[RouteSegment]]
