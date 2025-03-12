from datetime import datetime
from dataclasses import dataclass
@dataclass(init=False, repr=True, eq=True)
class Stock:
    __tablename__ = 'stocks'
    __table_args__ = {'schema':'ms_stocks'}
    
    id_stock: int
    id_product: int
    transaction_date: datetime = datetime.now()
    quantity: float
    in_out: int
    active:bool = True