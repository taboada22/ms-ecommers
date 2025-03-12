from dataclasses import dataclass
from app.Models.product import Product

@dataclass
class Cart:
    product: Product
    shipping_address: str
    quantity: int
    payment_mode: str
