from fastapi import FastAPI
from enum import Enum

app =  FastAPI()

@app.get("/")
def read_root():
    return {"mensaje" : "Guten Morgen!"}

# Path parameters
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"ItemID" : item_id}

# Importancia del orden de rutas: primero, las fijas y luego, variables
@app.get("/users/me")
def read_current_user():
    return {"Usuario" : "Samuel"}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"ItemID" : user_id}

# Tipos restringidos (enums)
class Modelo(str, Enum):
    modelo_a = "Modelo A"
    modelo_b = "Modelo B"
    modelo_c = "Modelo C"

@app.get("/modelos/{nombre_modelo}")
def obtener_modelo(nombre_modelo: Modelo):
    return {"modelo" : nombre_modelo}
