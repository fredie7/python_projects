from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from .models import Category, MenuItem, Cart, Order, OrderItem
from decimal import Decimal
from datetime import date

class CategoryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.client = APIClient()

    def test_get_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_category(self):
        self.client.login(username='tarik', password='tarikpass')
        data = {'slug': 'cheese', 'title': 'Cheese'}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MenuItemTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Coke', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()

    def test_get_menu_items(self):
        response = self.client.get(reverse('menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_menu_item(self):
        self.client.login(username='tarik', password='tarikpass')
        data = {'title': 'Jack Daniels', 'price': Decimal('1.50'), 'featured': False, 'category': self.category.id}
        response = self.client.post(reverse('menuitem-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CartTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Jack Daniels', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')

    def test_get_cart(self):
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart(self):
        data = {'menuItem': self.menuItem.id, 'quantity': 2, 'unitPrice': Decimal('1.50'), 'price': Decimal('3.00')}
        response = self.client.post(reverse('cart-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class OrderTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.category = Category.objects.create(slug='pizzas', title='Pizzas')
        self.menuItem = MenuItem.objects.create(title='Coke', price=Decimal('1.50'), featured=True, category=self.category)
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')

    def test_get_orders(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        Cart.objects.create(user=self.user, menuItem=self.menuItem, quantity=2, unitPrice=Decimal('1.50'), price=Decimal('3.00'))
        data = {'status': True, 'date': str(date.today())}
        response = self.client.post(reverse('order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GroupTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tarik', password='tarikpass')
        self.group = Group.objects.create(name='Manager')
        self.client = APIClient()
        self.client.login(username='tarik', password='tarikpass')

    def test_add_user_to_group(self):
        data = {'username': 'tarik'}
        response = self.client.post(reverse('group-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_user_from_group(self):
        data = {'username': 'tarik'}
        response = self.client.delete(reverse('group-list'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
