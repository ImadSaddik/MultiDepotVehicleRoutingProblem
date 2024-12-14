import pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from optimizer import get_optimized_routes
from clustering import assign_employees_to_buses
from models import OptimizeRequest


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('./routes.pkl', 'rb') as f:
    routes = pickle.load(f)


@app.post("/api/v1/optimize/")
async def optimize_route(request: OptimizeRequest):
    data = get_data_in_expected_format(
        request=request
    )

    employees_to_bus_clusters = assign_employees_to_buses(
        buses_data=data["buses_data"],
        employees_data=data["employees_data"],
        routes=routes,
    )
    optimized_routes = get_optimized_routes(
        employees_to_bus_clusters=employees_to_bus_clusters,
        buses_data=data["buses_data"],
        employees_data=data["employees_data"],
        company_location=data["company_data"],
        routes=routes,
    )
    return optimized_routes


def get_data_in_expected_format(request: OptimizeRequest) -> dict:
    solver_method = request.solver
    buses_data = [(bus_data.latitude, bus_data.longitude)
                  for bus_data in request.buses_data]
    employees_data = [(employee_data.latitude, employee_data.longitude)
                      for employee_data in request.employees_data]
    company_data = (request.company_data.latitude,
                    request.company_data.longitude)
    return {
        "solver_method": solver_method,
        "buses_data": buses_data,
        "employees_data": employees_data,
        "company_data": company_data,
    }
