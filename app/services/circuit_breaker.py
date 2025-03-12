import time
from app.Services.builder import BuilderServices
from app.Models.cart import Cart


class CircuitBreaker:
    def __init__(self):
        self.time_timeout = 5
        self.max_fails = 3
        self.fails = 0
        self.closed = True


    def call(self, cart: Cart):
        if self.closed:
            try:
                builder = BuilderServices()
                builder.buy_saga(cart)
                self.reset()
                status_code = 200
                return status_code
            except TimeoutError:
                self.fail_registry()
                status_code = 500
                return status_code
        else:
            raise BaseException("Unreachable Code")
        
    def reset(self):
        self.fails = 0
        self.closed = True

    def fail_registry(self):
        self.fails += 1
        if self.fails == self.max_fails:
            self.closed = False
            self.time_timeout = time.time()

    