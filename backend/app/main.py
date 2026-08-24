from fastapi import FastAPI
from routers import productos, tareas, usuarios

app =  FastAPI(title="Mi API")

app.include_router(productos.router, prefix="/api/v1")
app.include_router(tareas.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
