from app import ma

class CartSchema(ma.Schema):
    class Meta:
        fields = ('product', 'shipping_address', 'quantity', 'payment_mode')

cart_schema = CartSchema()
