from marshmallow import fields, Schema, post_load
from app.models.purchase import Purchase

class PurchaseSchema(Schema):
    id_purchase = fields.Integer(required=False)
    id_product = fields.Integer(required=True)
    mailing_address = fields.String(required=True)
    date_purchase = fields.DateTime(required=False)
    deleted_at = fields.DateTime(required=False, allow_none=True)
    

    @post_load
    def make_compra(self, data, **kwargs):
        compra = Purchase()
        for key, value in data.items():
            setattr(compra, key, value)
        return compra
        