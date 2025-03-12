import logging
from flask import Blueprint, jsonify, request
from app.Models.cart import Cart
from app.Models.product import Product
from app.Services.format_logs import format_logs
from app.Services.product import LinkedProducts
from app.Services.builder import BuilderServices
from app.Schemas.cart import CartSchema
from app.Services.circuit_breaker import CircuitBreaker

logging = format_logs('BuilderRoute')
builder = Blueprint('builder', __name__, url_prefix='/api/commerce')
cart_schema = CartSchema()

@builder.route('/buy', methods=['POST'])
def buy():
    circuit_breaker = CircuitBreaker()
 
    data = cart_schema.load(request.json)
    cart = Cart(**data)
    args = data['product']
    product = Product(**args)
    cart.product = product
   
    ans = circuit_breaker.call(cart)

    if ans == 200:
        res = jsonify({"microservice": "Builder", "status": "OK"})
        res.status_code = 200
        return res
    else:
        res = jsonify({"microservice": "Builder", "status": "ERROR"})
        res.status_code = 500
        return res
