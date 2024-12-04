from dataclasses import dataclass

@dataclass(repr=True, eq=True)
class Producto:
    id_producto: int 
    nombre: str
    precio: float
    activado: bool
