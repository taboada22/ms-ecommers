import os, requests
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_fixed
from app import cache
from app.Services.format_logs import format_logs
from app.Models.product import Product
from app.Schemas.product import product_schema, products_schema

logging = format_logs('LinkedProductService')

@dataclass
class LinkedProducts():
    URL = os.getenv('PRODUCTS_URL')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def get_product_by_id(self, id: int) -> Product:
        cached = cache.get(f'product_{id}')
        if cached:
            logging.info(f'product_{id} cached in ms-products')
            return cached
        else:
            req = requests.get(f'{self.URL}/get_by_id/{id}')
            if req.status_code == 200:
                cache.set(f'product_{id}', req.json())
                logging.info(f'product_{id} active, and cached')
                return product_schema.load(req.json())
            else:
                logging.error('Error in request ms-products')
                raise BaseException('Error in ms-products')