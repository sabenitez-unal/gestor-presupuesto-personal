from enum import Enum
from pydantic import BaseModel, Field

class TipoDocumento(str, Enum):
    cedula_ciudadania = "Cédula de Ciudadanía"
    cedula_extranjeria = "Cédula de Extranjería"
    tarjeta_identidad = "Tarjeta de Identidad"
    pasaporte = "Pasaporte"

# Modelo pydantic para procesar los datos de una peticion bajo una forma específica, usados en endpoints POST mas abajo
class Persona(BaseModel):   # Modelo de persona
    nombre: str = Field(min_length=2, max_length=50)
    apellido: str = Field(max_length=50)
    tipo_documento: TipoDocumento
    sobre_mi: str | None = Field(default=None, max_length=200)

class PersonaCreated(Persona):
    documento: str = Field(min_length=8, max_length=10, pattern="^[0-9]+$")

class PersonaSalida(Persona):
    documento: str = Field(min_length=8, max_length=10)
