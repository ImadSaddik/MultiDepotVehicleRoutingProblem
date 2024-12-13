import pickle

from typing import List
from pydantic import BaseModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/api/v1/optimize/")
async def optimize_route(request: OptimizeRequest):
    solver_method = request.solver
    employees_data = request.employees_data
    buses_data = request.buses_data
    company_data = request.company_data

    return {"status": "ok"}
