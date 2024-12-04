import unittest
from marshmallow import ValidationError
from app.schemas import CartSchema
from app.models import ShoppingCart

class TestCartSchema(unittest.TestCase):
    def setUp(self):
        self.schema = CartSchema()

    def test_valid_data(self):
        valid_data = {
            "id_product": 15,
            "mailing_address": "jose paez",
            "amount": 12.0,
            "means_of_payment": "yolo"
        }
        result = self.schema.load(valid_data)
        self.assertIsInstance(result, ShoppingCart)
        self.assertEqual(result.id_product, 15)
        self.assertEqual(result.mailing_address, "jose paez")
        self.assertEqual(result.amount, 12.0)
        self.assertEqual(result.means_of_payment, "yolo")

    def test_invalid_data(self):
        invalid_data = {
            "id_product": "not_an_int",  # Invalid type
            "mailing_address": "jose paez",
            "amount": 12.0,
            "means_of_payment": "yolo"
        }
        with self.assertRaises(ValidationError):
            self.schema.load(invalid_data)

    def test_missing_field(self):
        missing_field_data = {
            "id_product": 15,
            "amount": 12.0,
            "means_of_payment": "yolo"
        }
        with self.assertRaises(ValidationError):
            self.schema.load(missing_field_data)

if __name__ == '__main__':
    unittest.main()