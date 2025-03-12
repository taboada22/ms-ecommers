from app import ma

class PurchaseSchema(ma.Schema):
    class Meta:
        fields = ('id_purchase', 'id_product', 'purchase_date', 'shipping_address', 'active', 'deleted')

purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)