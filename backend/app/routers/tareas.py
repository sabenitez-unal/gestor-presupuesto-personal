from fastapi import APIRouter
from schemas.tarea import TareaResponse, Tarea

router = APIRouter(
    prefix="/router",
    tags=["tareas"]
)

# Almacenamiento de tareas ----volátil----
tareas: list[TareaResponse] = []
counter = 0

# Creacion de tarea
@router.post("/tareas", response_model=TareaResponse)
def crear_tarea(tarea: Tarea):
    global counter
    nueva_tarea = TareaResponse(id=counter, **tarea.model_dump())
    tareas.append(nueva_tarea)
    counter += 1
    return nueva_tarea
