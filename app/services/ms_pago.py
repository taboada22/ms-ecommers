import logging
import requests
import os
from tenacity import retry, wait_random, stop_after_attempt   
from app.models.paymet import Paymet
from app.models.product import Producto
from app.schemas.paymet import PaymetSchema
from app.services.ms_catalogo import MsCatalogo

class MsPago:
    def __init__(self) -> None:
        self.paymet = Paymet()
        self.URL = os.getenv('URL_MS_PAGO')
        self.ms_catalogo = MsCatalogo()

    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))       
    def register_paymet(self, id_product, means_of_payment:str, amount):
        self.paymet.id_product = id_product
        producto = self.ms_catalogo.get_by_id(id_product)
        self.paymet.price =  amount * producto.precio
        self.paymet.means_of_payment = means_of_payment
        paymet_schema = PaymetSchema()
        data_paymet = paymet_schema.dump(self.paymet)
        resp = requests.post(f'{self.URL}/addpaymet', json=data_paymet)
        
        if resp.status_code == 200:
            logging.info(f"Pago realizado")
        else:
            logging.error(f"Error al realizar el pago {resp.status_code}")
            raise BaseException("Error en el microservicio de pagos")
    @retry(wait=wait_random(min=1, max=2), stop=stop_after_attempt(3))     
    def cancel_paymet(self):
        try:
            if self.paymet.id_paymet:
                resp = requests.put(f'{self.URL}/delete/{self.paymet.id_paymet}')
                if resp.status_code == 200:
                    logging.warning(f"Pago cancelado")
                    self.paymet = Paymet()
                else: 
                    logging.error(f"Error al cancelar el pago")
                    raise BaseException("Error al cancelar el pago")
        except:
            logging.error(f"Error cancelar el pago no se encontro id")
            raise BaseException("Error no se pudo cancelar el pago, no se encontro id")
    