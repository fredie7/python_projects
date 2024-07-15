# Import dependencies

from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem, Category
from django.contrib.auth.models import User

# Serialize the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        
        # Fields to be serialized
        fields = ['id', 'slug', 'title']

# Serialize the MenuItem model
class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        
        # Relate MenuItem to Category
        queryset=Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
# Serialize the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Serialize the Cart model
class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        
        # Relate Cart to User
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuItem', 'quantity', 'unitPrice', 'price']

# Serialize the OrderItem model
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuItem', 'quantity', 'price']

# Serialize the Order model
class OrderSerializer(serializers.ModelSerializer):
    # Include related order items
    orderItems = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'deliveryCrew', 'status', 'date', 'total', 'orderItems']
