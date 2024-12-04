from datetime import date
import logging
from marshmallow import ValidationError
import requests
import os
from tenacity import retry, wait_random, stop_after_attempt   
from app.models.purchase import Purchase
from app.models.product import Producto
from app.schemas.purchase_schema import PurchaseSchema
from app.services.ms_inventario import MsInventario
from app.models.shopping_cart import ShoppingCart

class MsCompra:
    def __init__(self) -> None:
        self.purchase = Purchase()
        self.URL_MS_COMPRA = os.getenv('URL_MS_COMPRA', 'http://mscompras:5601/api/compra') 
        self.inventario = MsInventario()
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))
    def resgister_purchase(self, id_product: int, mailing_address: str, amount):
        if not id_product or not mailing_address:  
            logging.error("id_product o mailing_address no pueden ser vacíos.")  
            raise ValueError("id_product y mailing_address son obligatorios.") 
        self.purchase.id_product = id_product
        self.purchase.mailing_address = mailing_address
        check = self.inventario.check_stock(self.purchase.id_product, amount)
        if check != 'La cantidad es suficiemte' :
            raise BaseException("Error no hay suficiente stock para completar la compra.")
        purchase_schema = PurchaseSchema()
        
        resp = requests.post(f'{self.URL_MS_COMPRA}/addpurchase', json=purchase_schema.dump(self.purchase), verify= False)
        if resp.status_code == 200:
            logging.info(f"Compra enviada")
            logging.debug(f"Respuesta del microservicio: {resp.json()}")
           
            self.purchase = purchase_schema.load(resp.json())
            logging.info(f"Exito al comprar id: {self.purchase.id_purchase}")
            self.purchase = Purchase()
        else:
            logging.error(f"Error al comprar en el microservicios de compra.")
            raise BaseException("Error al comprar en el microservicios de compra.")
        
     
    def delete_purchase(self):
  
        if not self.purchase.id_purchase:
            logging.error("No se puede cancelar una compra sin id")
            raise BaseException("No se puede cancelar una compra sin id")
        resp = requests.delete(f'{self.URL_MS_COMPRA}/delete/{self.purchase.id_purchase}')
        if resp.status_code == 200:
            logging.warning(f"Compra eliminada")
        else: 
            logging.error(f"Error al eliminar la compra")
            raise BaseException("Error al eliminar la compra")



