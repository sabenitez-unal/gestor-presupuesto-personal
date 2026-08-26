from fastapi import APIRouter, status, HTTPException
from schemas.tarea import TareaResponse, Tarea

router = APIRouter(
    prefix="/router",
    tags=["tareas"]
)

# Almacenamiento de tareas ----volátil----
tareas: list[TareaResponse] = []
counter = 0

# Creacion de tarea
@router.post("/tareas", response_model=TareaResponse, status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea):
    # Comprobar duplicados
    for t in tareas:
        if t.titulo == tarea.titulo: 
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La tarea '{tarea.titulo}' ya existe."
            )

    global counter
    nueva_tarea = TareaResponse(id=counter, **tarea.model_dump())
    tareas.append(nueva_tarea)
    counter += 1
    return nueva_tarea
