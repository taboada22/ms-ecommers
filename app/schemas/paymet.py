from marshmallow import validate, fields, Schema, post_load
from app.models.paymet import Paymet

class PaymetSchema(Schema):
    id_paymet = fields.Integer(required=False)
    id_product = fields.Integer(required=False)
    price = fields.Float(required=False)
    means_of_payment = fields.String(required=False)
    deleted_at = fields.DateTime(required=False, allow_none=True)

    @post_load
    def make_pago(self, data, **kwargs):
        pago = Paymet()
        for key, value in data.items():
            setattr(pago, key, value)
        return pago
