from pydantic import BaseModel, Field

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

# Modelo de respuesta
class TareaResponse(Tarea):
    id: int
