from dataclasses import dataclass
from datetime import datetime


@dataclass(init=False, repr=True, eq=True)
class Stock():
    id_stock: int
    id_product: int
    date_transaction: datetime
    amount: int
    input_output: int