from fastapi import APIRouter, Path
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

# Enlistado de productos
@router.get("/", response_model=list[ProductoSalida])
def listar_productos():
    return productos

# Obtener un producto específico
@router.get("/{product_id}", response_model=ProductoSalida)
def leer_producto(producto_id: Annotated[int, Path(title="ID de Producto", ge=0)]):
    for p in productos:
        if p.id == producto_id: return p
    return {"err": "Not Found. :("} # <-- Pendiente de mirar manejo de errores HTTP

# Agregar un nuevo producto
@router.post("/", response_model=ProductoSalida)
def nuevo_producto(producto: Producto):
    global counter
    nuevo_producto = ProductoSalida(id=counter, **producto.model_dump(), disponibilidad=True)
    productos.append(nuevo_producto)
    counter += 1
    return nuevo_producto
