from marshmallow import validate, fields, Schema, post_load
from app.models.stock import Stock

class StockSchema(Schema):
    id_stock = fields.Integer(required=False)
    id_product = fields.Integer(required=True)
    date_transaction = fields.DateTime(required=False, allow_none=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    input_output = fields.Integer(required=True, validate=validate.OneOf([1, 2]))

    @post_load
    def make_stock(self, data, **kwargs):
        stock = Stock()
        for key, value in data.items():
            setattr(stock, key, value)
        return stock