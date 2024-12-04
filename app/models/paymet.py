from dataclasses import dataclass
import datetime


@dataclass(init=False, repr=True, eq=True)
class Paymet:
    id_paymet: int
    id_product: int
    price: float
    means_of_payment: str
    deleted_at: datetime
