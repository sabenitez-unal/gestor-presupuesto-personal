from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated

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


#----- Query Parameters --------#
# Parametros dentro de la URL que no son rutas

class Status(str, Enum):
    de_buenas = "de buenas"
    de_malas = "de malas"

@app.get("/{persona}")
def read_description(persona: str, status: Status):
    if persona.strip().lower() == "jhon":
        if status == "de malas":
            return f"{persona.capitalize()} está muy de malas y le toca las migajas de probabilidad :(."
        return f"{persona.capitalize()} está muy de buenas y va a cinquearse proba."
    return f"No sé quién sea usted, señor/a {persona.capitalize()}"

@app.get("/numero/{numero}")
def read_numero(
    numero: Annotated[int, Path(title="El Numero", ge=0)],
    message: Annotated[str | None, Query(min_length=1, max_length=20)] = None
): 
    return {"numero":numero, "mensaje":message}

@app.get("/productos/{product_id}")
def read_product(
    product_id: Annotated[int, Path(title="ID de Producto", gt=0)],
    nombre: Annotated[str | None, Query(min_length=3)] = None,
    disponible: bool = True
):
    return {"ID Producto":product_id, "Nombre":nombre, "Disponible":disponible}
