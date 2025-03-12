import logging
from saga import SagaBuilder, SagaError
from tenacity import retry, stop_after_attempt, wait_fixed
from app.Models import Cart
from app.Services.format_logs import format_logs
from app.Services.payments import LinkedPayment
from app.Services.product import LinkedProducts
from app.Services.stock import LinkedStocks
from app.Services.purchases import LinkedPurchase

logging = format_logs('BuilderServices')

client_purchase = LinkedPurchase()
client_payment = LinkedPayment()
client_product = LinkedProducts()
client_stock = LinkedStocks()

class BuilderServices:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    def buy_saga(self, cart: Cart) -> None:
        try:
            SagaBuilder\
            .create()\
            .action(lambda: client_purchase.buy(cart.product, cart.shipping_address), lambda: client_purchase.cancel_purchase())\
            .action(lambda: client_payment.registry_payment(cart.product, cart.payment_mode), lambda: client_payment.cancel_payment())\
            .action(lambda: client_stock.add_product_to_cart(cart), lambda: client_stock.return_product_to_stock())\
            .build()\
            .execute()
            logging.info('Builder executed succefully')
        except SagaError as e:
            logging.error(f'Error en el Builder: {e}')