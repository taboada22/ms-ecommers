from dataclasses import dataclass
@dataclass(init=False, repr=True, eq=True)
class Payment:
    
    id_payment: int
    id_product: int
    amount: float
    payment_mode: str
    active: bool = True