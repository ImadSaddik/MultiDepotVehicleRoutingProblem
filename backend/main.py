import psycopg2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Node, OptimizeResponse
from optimizer import get_optimized_routes
from clustering import assign_employees_to_buses


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = psycopg2.connect(
    dbname='routes',
    user='postgres',
    password='postgres',
    host='localhost'
)
connection.autocommit = True
cursor = connection.cursor()


@app.post("/api/v1/optimize/")
async def optimize_route() -> OptimizeResponse:
    bus_nodes, employee_nodes, company_node = _get_nodes()

    employees_to_bus_clusters = assign_employees_to_buses(
        bus_nodes=bus_nodes,
        employee_nodes=employee_nodes,
        cursor=cursor
    )
    optimized_routes = get_optimized_routes(
        employees_to_bus_clusters=employees_to_bus_clusters,
        company_node=company_node,
        cursor=cursor
    )
    return optimized_routes


def _get_nodes() -> tuple:
    cursor.execute("""
    SELECT * FROM nodes
    """)

    data = cursor.fetchall()
    nodes = [Node(id=row[0], latitude=row[1], longitude=row[2], type_=row[3])
            for row in data]
    
    bus_nodes = [node for node in nodes if node.type_ == 'bus']
    employee_nodes = [node for node in nodes if node.type_ == 'employee']
    company_node = [node for node in nodes if node.type_ == 'company'][0]
    
    return bus_nodes, employee_nodes, company_node
