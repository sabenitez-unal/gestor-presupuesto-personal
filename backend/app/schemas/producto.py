from enum import Enum
from pydantic import BaseModel, Field

#Modelo anidado, Image dentro de Item
class Imagen(BaseModel):
    url: str
    nombre_alt: str = Field(max_length=100)

# Modelo de un producto, con field() para restricciones
class Producto(BaseModel):      
    nombre: str = Field(min_length=3, max_length=50)
    precio: float = Field(gt=0, description="Debe ser mayor que cero ($0)")
    descripcion: str | None = Field(default=None, max_length=300)
    imagen: list[Imagen] | None = None # Lista de diccionarios que siguen el modelo Image, es opcional, pero de existir debe seguir el modelo Image
    en_oferta: bool = False

# Modelo para respuesta de API
class ProductoSalida(Producto):
    id: int
    disponibilidad: bool
