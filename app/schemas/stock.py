from app import ma

class StockSchema(ma.Schema):
    class Meta:
        fields = ('id_stock', 'id_product', 'transaction_date', 'quantity', 'in_out', 'active')

stock_schema = StockSchema()
stocks_schema = StockSchema(many=True)