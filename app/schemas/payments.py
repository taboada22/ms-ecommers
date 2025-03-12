from app import ma

class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('id_payment', 'id_product', 'amount', 'payment_mode', 'active')

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)