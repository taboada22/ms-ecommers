from dataclasses import dataclass
from datetime import datetime
@dataclass(init=False, repr=True, eq=True)
class Purchase:
    __tablename__ = 'purchases'
    __table_args__ = {'schema':'ms_purchases'}
    
    id_purchase: int 
    id_product: int
    purchase_date: datetime = datetime.now()
    shipping_address: str
    active: bool = True
    deleted: bool = False