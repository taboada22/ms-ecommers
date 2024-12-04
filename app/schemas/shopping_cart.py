from marshmallow import fields, Schema, post_load
from app.models import ShoppingCart

class CartSchema(Schema):
    id_product = fields.Integer(required=True)
    mailing_address = fields.String(required=True)
    amount = fields.Float(required=True)
    means_of_payment = fields.String(required=True)

    @post_load
    def make_shopping_cart(self, data, **kwargs):
        return ShoppingCart(**data)