from app import ma

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id_product', 'name', 'price', 'active')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)