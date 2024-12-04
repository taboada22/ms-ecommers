import requests
import os
from tenacity import retry, wait_random, stop_after_attempt       
from app.models import Producto
from app.schemas.product import ProductoSchema
from app import cache

producto_schema = ProductoSchema()

class MsCatalogo:
    
    def __init__(self) -> None:
        self.URL_MS_CATALOGO = os.getenv('URL_MS_CATALOGO', 'http://127.0.0.1:5600/api/producto')
        
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def get_by_id(self, id: int) -> Producto:
        producto = None
        resp = requests.get(url=f'{self.URL_MS_CATALOGO}/find_by_id/{id}')
        if resp.status_code == 200:
            producto = producto_schema.load(resp.json())
            cache.set(f'producto_id_{id}', producto, timeout=30)
        else:
            raise Exception('Microservicio Catálogo ha fallado.')
        
        return producto