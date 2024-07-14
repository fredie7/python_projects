from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from ..models import Menu
from ..serializers import MenuSerializer
from django.test import TestCase

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a user
        self.user = User.objects.create_user(username='fred', password='fredtoken')
        
        # Obtain user token
        self.token = Token.objects.create(user=self.user)
        
        # Authenticate user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create test menu items
        self.menu_item_1 = Menu.objects.create(title="Dish 1", price=9.99, inventory=50)
        self.menu_item_2 = Menu.objects.create(title="Dish 2", price=19.99, inventory=30)
        self.menu_item_3 = Menu.objects.create(title="Dish 3", price=29.99, inventory=20)

    def test_get_menu_items(self):
        response = self.client.get(reverse('menu-items'))
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
