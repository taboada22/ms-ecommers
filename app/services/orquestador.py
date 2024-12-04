import logging  
from saga import SagaBuilder, SagaError  
from app.services import MsPago, MsCatalogo, MsCompra, MsInventario  
from app.models import ShoppingCart  

# Inicialización de los servicios  
customerPurchases = MsCompra()  
customerPayments = MsPago()  
customerStock = MsInventario()  
customerProduct = MsCatalogo()  

import logging  

class CommerceService:  
    def comprar(self, cart: ShoppingCart) -> bool:  
        try:  
            logging.info("Iniciando proceso de compra...")  
            if not isinstance(cart, ShoppingCart):  
                logging.error("El objeto cart no es una instancia de ShoppingCart.")  
                return False  

            logging.info("Registro de compra para el producto ID: %s", cart.id_product)  
            SagaBuilder.create()\
                .action(  
                    lambda: customerPurchases.resgister_purchase(cart.id_product, cart.mailing_address, cart.amount),   
                    lambda: customerPurchases.delete_purchase()  
                ) \
                .action(  
                    lambda: customerPayments.register_paymet(cart.id_product, cart.means_of_payment, cart.amount),   
                    lambda: customerPayments.cancel_paymet()  
                ) \
                .action(  
                    lambda: customerStock.whitdraw_product(cart),   
                    lambda: customerStock.enter_product())\
                .build()\
                .execute()  
            return True  
        except SagaError as e:  
            logging.error("Error en la compra: %s", e)  
            return False