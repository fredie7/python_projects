# Import dependencies

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from .models import Category, MenuItem, Cart
from decimal import Decimal
from datetime import date

# Test cases for Category model
class CategoryTests(APITestCase):

    def setUp(self):

        # prepare a user and corresponding category for testing
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.client = APIClient()

    # Test retrieving list of categories
    def test_get_categories(self):        
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test creating a new category
    def test_create_category(self):
        self.client.login(username='tarik', password='tarikpass')
        data = {'slug': 'cheese', 'title': 'Cheese'}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Test cases for MenuItem model
class MenuItemTests(APITestCase):

    # prepare a user, category, and corresponding menu item for testing
    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Coke', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()

    # Test retrieving list of menu items
    def test_get_menu_items(self):
        response = self.client.get(reverse('menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test creating a new menu item
    def test_create_menu_item(self):
        self.client.login(username='tarik', password='tarikpass')
        data = {'title': 'Jack Daniels', 'price': Decimal('1.50'), 'featured': False, 'category': self.category.id}
        response = self.client.post(reverse('menuitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Test cases for Cart model
class CartTests(APITestCase):

    # Prepare a user, category, and corresponding menu item for testing
    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Jack Daniels', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')
    
    # Test retrieving the cart items
    def test_get_cart(self):
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test adding a menu item to the cart
    def test_add_to_cart(self):
        data = {'menuItem': self.menuItem.id, 'quantity': 2, 'unitPrice': Decimal('1.50'), 'price': Decimal('3.00')}
        response = self.client.post(reverse('cart-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Test cases for Order model
class OrderTests(APITestCase):
    
    # Setup a user, a category, and a menu item for testing
    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Coke', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')

    # Test retrieving list of orders
    def test_get_orders(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Test creating a new order from items in the cart
    def test_create_order(self):
        Cart.objects.create(user=self.user, menuItem=self.menuItem, quantity=2, unitPrice=Decimal('1.50'), price=Decimal('3.00'))
        data = {'status': True, 'date': str(date.today())}
        response = self.client.post(reverse('order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# Test cases for Group model
class GroupTests(APITestCase):

     # Prepare a user and corresponding group for testing
    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.group = Group.objects.create(name='Manager')
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')

    # Test adding a user to the Manager group
    def test_add_user_to_group(self):
        data = {'username': 'tarik'}
        response = self.client.post(reverse('group-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

     # Test removing a user from the Manager group
    def test_remove_user_from_group(self):
        data = {'username': 'tarik'}
        response = self.client.delete(reverse('group-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
