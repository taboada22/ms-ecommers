from dataclasses import dataclass
@dataclass(repr=True, eq=True)
class Product:
    __tablename__ = 'products'
    __table_args__ = {'schema': 'ms_products'}
    
    id_product: int
    name: str
    price: float
    active: bool = True