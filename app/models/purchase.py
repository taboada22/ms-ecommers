from dataclasses import dataclass
from datetime import datetime

@dataclass(init=False, repr=True, eq=True)
class Purchase:  
    id_purchase : int #= None
    id_product : int #= None
    mailing_address : str #= None
    date_purchase : datetime #= None
    deleted_at: datetime #= None
    

