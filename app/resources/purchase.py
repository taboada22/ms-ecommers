import logging
from app.services.cicuit_braker import CircuitBreaker
from flask import jsonify, Blueprint, request
from marshmallow import ValidationError

from app.schemas import CartSchema, ProductoSchema
from app.services import CommerceService

purchase = Blueprint('compra', __name__, url_prefix='/api/comercio')  
cart_schema = CartSchema()

@purchase.route('/commerce/comprar', methods=['POST'])
def compra():
    commerce = CircuitBreaker()
    try:
        datos_compra = request.get_json()
        cart = cart_schema.load(datos_compra)
        success = commerce.call(cart)

        if success:
            resp = cart_schema.dump(cart), 200
        else:
            resp = jsonify('PROCESO DE COMPRA HA FALLADO :('), 400 
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400  
    except Exception as e:
        logging.error(f"Error en la compra: {e}")
        return jsonify({"error": "Error del servicio"}), 500  

    return resp