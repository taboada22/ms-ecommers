import logging
import requests
import os
from datetime import date
from tenacity import retry, wait_random, stop_after_attempt   
from app.models.stock import Stock
from app.models.shopping_cart import ShoppingCart
from app.schemas.stock import StockSchema
from app import cache

class MsInventario:
    
    def __init__(self) -> None:
        self.stock= Stock()    
        self.URL_MS = os.getenv('URL_MS_INVENTARIO', 'http://msinvenatio:5602/api/stock')
        
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def whitdraw_product(self, cart: ShoppingCart) -> None:
        self.stock.id_product = cart.id_product
        self.stock.amount = cart.amount
        self.stock.input_output = 2
        stock_schema = StockSchema()
        data_stock = stock_schema.dump(self.stock)
        resp = requests.post(f'{self.URL_MS}/whitdraw', json=data_stock)
        if resp.status_code == 200:
            logging.info(f"stock registrado con exito")
            self.stock = stock_schema.load( resp.json() )
            logging.info(f"Stock registrado id: {self.stock.id_stock}")
            self.stock= Stock()   
        else:
            logging.error(f"Error al registrar stock {resp.status_code}")
            raise BaseException("Error al registrar en el microservicio de stock")

    
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def enter_product(self) -> None:
 
        if not self.stock.id_stock:           
            logging.error("No se puede ingresar Stock sin id")
            raise BaseException("No se puede ingresar Stock sin id")
        
        self.stock.input_output = 1
        resp = requests.post(f'{self.URL_MS}/enter_product/{self.stock.id_stock}')
        if resp.status_code == 200:
            logging.info(f"stock ingresado")
            self.stock= Stock()   
        else:
            logging.error(f"Error al ingresar stock {resp.status_code}")
            raise BaseException("Error al registrar en el microservicio de stock")

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))   
    def check_stock(self, id_product, amount) -> None:       
        self.stock.id_product = id_product
        self.stock.amount = amount
        resp = requests.get(f'{self.URL_MS}/calculate_stock/{self.stock.id_product}')
        if resp.status_code == 200:
            data_stock = resp.json()
            stock = cache.get(f'data_stock_{resp}')
            if data_stock['total_stock'] >= self.stock.amount:
                logging.info(f"La cantidad es suficiemte.")   
                return 'La cantidad es suficiemte'            
            else:
                raise BaseException(f"Insuficiente stock del producto")
        else:
            raise BaseException('Fallo en microservicio inventario.')