from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field

app =  FastAPI()

# Modelo pydantic para procesar los datos de una peticion bajo una forma específica, usados en endpoints POST mas abajo
class Persona(BaseModel):   # Modelo de persona
    nombre: str
    apellido: str
    documento: int
    sobre_mi: str | None = None

#Modelo anidado, Image dentro de Item
class Image(BaseModel):
    url: str
    nombre_alt: str = Field(max_length=100)

class Item(BaseModel):      # Modelo de un producto, con field() para restricciones
    nombre: str = Field(min_length=3, max_length=50)
    precio: float = Field(gt=0, description="Debe ser mayor que cero ($0)")
    descripcion: str | None = Field(default=None, max_length=300)
    imagen: list[Image] | None = None # Lista de diccionarios que siguen el modelo Image, es opcional, pero de existir debe seguir el modelo Image
    en_oferta: bool = False

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

# Tipos restringidos (enums) -> El path o query parameter sólo puede ser uno de ellos.
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

# Una nueva persona segun el modelo y otros elementos
@app.post("/personas", status_code=201)
def nueva_persona(
    persona: Persona,
    vigente: Annotated[bool, Query()]
):
    return {"id":1, **persona.model_dump(), "¿vigente?": vigente}

@app.get("/personas/{id_persona}")
def read_description(persona: str, status: Status):
    if persona.strip().lower() == "jhon":
        if status == "de malas":
            return f"{persona.capitalize()} está muy de malas y le toca las migajas de probabilidad :(."
        return f"{persona.capitalize()} está muy de buenas y va a cinquearse proba."
    return f"No sé quién sea usted, señor/a {persona.capitalize()}"


# Acá Annotated es para definir correctamente el tipo de dato con restricciones que maneja FastAPI
# Path() para path parameters; Query() para query parameters
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


# --------Modelos Pydantic-----------#
# Modelos definidos al inicio
# Crear un item nuevo
@app.post("/items", status_code=201)
def crear_item(item: Item):
    return item.model_dump()

# Para modificar un item
@app.put("/items/{item_id}")
def actualizar_item(
    item_id: int,
    item: Item,
    q: str | None = None
):
    result = {"Item ID":item_id, **item.model_dump()}
    if q: result["q"] = q
    return result


# Como hacer para que la respuesta a una peticion POST tenga el mismo body
# Modelo para entrada
class UsuarioEntrada(BaseModel):
    email: str
    password: str

# Modelo para salidas
class UsuarioSalida(BaseModel):
    email: str
    user_id: int

# En la peticion, se especifica con qué modelo se va a responder
@app.post("/usuarios", response_model=UsuarioSalida, status_code=201)
def crear_usuario(usuario: UsuarioEntrada):
    return {"email":usuario.email, "user_id":1}



#Practica de modelos propuesta
# Modelo de etiquetas para tareas
class Etiqueta(BaseModel):
    nombre: str
    id_etiqueta: int

# Modelo para tareas
class Tarea(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    completada: bool = False
    prioridad: int = Field(ge=1, le=5)
    etiquetas: list[Etiqueta] | None = None

# peticion POST
@app.post("/tareas", status_code=201)
def nueva_tarea(
    tarea: Tarea
):
    return tarea
