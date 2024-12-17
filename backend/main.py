import redis
import psycopg2

from psycopg2.extensions import cursor

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import Node, OptimizeResponse
from optimizer import get_optimized_routes
from clustering import assign_employees_to_buses


redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/optimize/")
def optimize_route() -> OptimizeResponse:
    connection, cursor = _connect_to_postgres()
    bus_nodes, employee_nodes, company_node = _get_nodes(cursor=cursor)

    employees_to_bus_clusters = assign_employees_to_buses(
        bus_nodes=bus_nodes,
        employee_nodes=employee_nodes,
        cursor=cursor
    )
    optimized_routes = get_optimized_routes(
        employees_to_bus_clusters=employees_to_bus_clusters,
        company_node=company_node,
        cursor=cursor,
        redis_client=redis_client
    )

    redis_client.set("optimization_progress", 100)
    connection.close()
    cursor.close()
    return optimized_routes


def _connect_to_postgres() -> tuple:
    connection = psycopg2.connect(
        dbname='routes',
        user='postgres',
        password='postgres',
        host='localhost'
    )
    connection.autocommit = True
    cursor = connection.cursor()
    return connection, cursor


def _get_nodes(cursor: cursor) -> tuple:
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


@app.get("/api/v1/optimize/progress/")
def get_optimization_progress():
    progress = redis_client.get('optimization_progress')

    if progress is None:
        progress = 0

    return JSONResponse(content={"progress": int(progress)}, status_code=200)


@app.post("/api/v1/optimize/reset-progress/")
def reset_optimization_progress():
    redis_client.delete('optimization_progress')
    return JSONResponse(content={"message": "Progress reset successfully"}, status_code=200)
