from fastapi import APIRouter, Path, status, HTTPException
from typing import Annotated

# Esquemas
from schemas.producto import Producto, ProductoSalida

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

# Lista de productos ----Volátil----
productos: list[ProductoSalida] = []
counter = 0

# Agregar un nuevo producto
@router.post(
    "/", 
    response_model=ProductoSalida, 
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Product already exists"}}
)    # <- Solicitudes POST siempre entregan código 201 (Created)
def nuevo_producto(producto: Producto):
    # Comprobar duplicados
    for p in productos:
        if p.nombre == producto.nombre: 
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El producto '{producto.nombre}' ya existe."
            )

    # Si no hay duplicados, añadir.
    global counter
    nuevo_producto = ProductoSalida(id=counter, **producto.model_dump(), disponibilidad=True)
    productos.append(nuevo_producto)
    counter += 1
    return nuevo_producto

# Enlistado de productos
@router.get("/", response_model=list[ProductoSalida])
def listar_productos():
    return productos

# Obtener un producto específico
@router.get(
    "/{producto_id}", 
    response_model=ProductoSalida,
    responses={404: {"description":"Product was not found"}}
)
def leer_producto(producto_id: Annotated[int, Path(title="ID de Producto", ge=0)]):
    for p in productos:
        if p.id == producto_id: return p
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El producto especificado no existe."
    ) # <-- manejo de errores HTTP

# Eliminar algún recurso
@router.delete(
    "/{producto_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description":"Product was not found"}}
)
def eliminar_producto(producto_id: Annotated[int, Path(title="ID de Producto", ge=0)]):
    for i, p in enumerate(productos):   # <- Para tomar tanto elemento de la lista como su índice
        if p.id == producto_id: 
            productos.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El producto especificado no existe."
    )
