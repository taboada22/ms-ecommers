import os, requests
from dataclasses import dataclass
from app import cache
from app.Services.format_logs import format_logs
from app.Models.stock import Stock
from app.Schemas.stock import stock_schema
from app.Models.cart import Cart


logging = format_logs('LinkedStockService')

@dataclass
class LinkedStocks():
    url = os.getenv('STOCKS_URL')
    stock = Stock()

    # Retira un producto del stock y lo agrega al carrito de compras

    def add_product_to_cart(self, cart: Cart) -> None:

        self.stock.in_out = 2
        self.stock.id_product = cart.product.id_product
        res = requests.get(f'{self.url}/get_by_product/{cart.product.id_product}')
        stocks = stock_schema.loads(res.content)    # Cantidad que hay de un producto en stock
       
        if res.status_code == 200:
            if stocks['quantity'] >= cart.quantity:
                self.stock.quantity = stocks['quantity'] - cart.quantity

                #body = stock_schema.dumps(self.stock)   # Variable que carga el nuevo stock

                response = requests.put(f"{self.url}/update/{stocks['id_stock']}", json=stock_schema.dumps(self.stock))
                data = stock_schema.loads(response.content)

                if response.status_code == 201:
                    cache.set(f"stock_{data['id_product']}", data)
                    logging.info(f"Stock: {data['id_product']}\n{data}")
                else:
                    logging.error(f'Error in stock-ms')
                    raise BaseException('Error in stock-ms')
            else:
                logging.error(f'There is not enough stock for product {cart.product.id_product}')
                raise BaseException(f'There is not enough stock for product {cart.product.id_product}')
        
        
      


    # Devuelve el producto al stock y lo retira del carrito de compras

    def return_product_to_stock(self) -> None:
        # No necesita hacer nada porque sí no hay stock, no se graba en la DB el retiro,
        # tampoco en el caché; pero necesitamos la compensación en el builder, por ésta razón,
        # este método sólo retorna None
        
        pass
#--------------------------------------------------------------------------------------------------------
   