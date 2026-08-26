from fastapi import APIRouter, Path, status, HTTPException
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
@router.get(
    "/{documento}", 
    response_model=PersonaResponse,
    responses={404: {"description":"Usuario no encontrado"}}
)
def consultar_usuario(
    documento: Annotated[str, Path(title="No. Documento", min_length=8, max_length=10, pattern="^[0-9]+$")]
):
    for usuario in usuarios:
        if documento == usuario.documento: return usuario
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no existe."
    ) # <-- Pendiente de mirar manejo de errores HTTP

# Añadir nuevo usuario
@router.post(
    "/", 
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description":"El usuario ya existe"}}
)
def crear_usuario(usuario: PersonaCreated):
    for u in usuarios:
        if u.documento == usuario.documento:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Un usuario con el mismo documento ya existe."
            )
    # En caso de que no esté duplicado el documento
    nuevo_usuario = PersonaResponse(**usuario.model_dump())
    usuarios.append(nuevo_usuario)
    return nuevo_usuario
