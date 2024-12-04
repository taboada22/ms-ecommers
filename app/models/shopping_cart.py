from dataclasses import dataclass

from app.models.product import Producto

@dataclass

class ShoppingCart:  
    id_product: int
    mailing_address: str
    amount: float
    means_of_payment: str
    #id_purchase: int = None
    #id_paymet: int = None
    #price_paymet: float = None
    
    