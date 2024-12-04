import unittest  
from unittest.mock import patch, MagicMock  
from app.models import ShoppingCart  
from app.services import CommerceService  

class TestCommerceService(unittest.TestCase):  
    def setUp(self):  
        self.service = CommerceService()  
        self.cart = ShoppingCart(  
            id_product=15,  
            mailing_address="jose paez",  
            amount=12.0,  
            means_of_payment="yolo"  
        )  

    @patch('app.services.customerPurchases')  
    @patch('app.services.customerPayments')  
    @patch('app.services.customerStock')  
    def test_comprar_success(self, mock_customerStock, mock_customerPayments, mock_customerPurchases):  
     
        mock_customerPurchases.register_purchase.return_value = True  
        mock_customerPayments.register_payment.return_value = True  
        mock_customerStock.withdraw_product.return_value = True  

        # Llama al método comprar  
        success = self.service.comprar(self.cart)  

          
        self.assertTrue(success)  

        # Verifica que se llamaron a los métodos correctos  
        mock_customerPurchases.register_purchase.assert_called_once_with(self.cart.id_product, self.cart.mailing_address)  
        mock_customerPayments.register_payment.assert_called_once_with(self.cart.id_product, self.cart.means_of_payment, self.cart.amount)  
        mock_customerStock.withdraw_product.assert_called_once_with(self.cart)  

    @patch('app.services.customerPurchases')  
    @patch('app.services.customerPayments')  
    @patch('app.services.customerStock')  
    def test_comprar_failure(self, mock_customerStock, mock_customerPayments, mock_customerPurchases):  
        
        mock_customerPurchases.register_purchase.side_effect = Exception("Error en el registro de compra")  

        
        success = self.service.comprar(self.cart)  

       
        self.assertFalse(success)  

        # Verifica que se llamaron a los métodos correctos  
        mock_customerPurchases.register_purchase.assert_called_once_with(self.cart.id_product, self.cart.mailing_address)  
        mock_customerPayments.register_payment.assert_not_called()  # No debería llamarse si falla el registro de compra  
        mock_customerStock.withdraw_product.assert_not_called()  # No debería llamarse si falla el registro de compra  

if __name__ == '__main__':  
    unittest.main()