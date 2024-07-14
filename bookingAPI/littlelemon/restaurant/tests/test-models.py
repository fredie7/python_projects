from django.test import TestCase
from ..models import Menu

class MenuTest(TestCase):
    def test_create_menu(self):
        
        # Obtain Menu Items       
        menu_item = Menu.objects.create(title="Test Dish", price=10.99, inventory=100)
        
        # Assert the menu item is created and the string representation is correct        
        self.assertEqual(str(menu_item), "Test Dish : 10.99")
