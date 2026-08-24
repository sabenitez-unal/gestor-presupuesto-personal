from fastapi import APIRouter, Path
from typing import Annotated

# Esquemas
from schemas.usuario import PersonaCreated, PersonaResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

# Almacenamiento de usuarios ----volátil----
usuarios: list[PersonaResponse] = []

# Consultar lista de usuarios
@router.get("/", response_model=list[PersonaResponse])
def leer_usuarios():
    return usuarios

# Consultar un usuario en específico
@router.get("/{documento}", response_model=PersonaResponse)
def consultar_usuario(
    documento: Annotated[str, Path(title="No. Documento", min_length=8, max_length=10, pattern="^[0-9]+$")]
):
    for usuario in usuarios:
        if documento == usuario.documento: return usuario
    return {"err": "Not Found. :("} # <-- Pendiente de mirar manejo de errores HTTP

# Añadir nuevo usuario
@router.post("/", response_model=PersonaResponse)
def crear_usuario(usuario: PersonaCreated):
    nuevo_usuario = PersonaResponse(**usuario.model_dump())
    usuarios.append(nuevo_usuario)
    return nuevo_usuario
