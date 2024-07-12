from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem, Category
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuItem', 'quantity', 'unitPrice', 'price']

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: OrderItem
#         fields = ['order', 'menuItem', 'quantity', 'unitPrice', 'price']

# class OrderSerializer(serializers.ModelSerializer):
#     orderItem = OrderItemSerializer(many=True, read_only=True, source='order')
#     class Meta:
#         model: Order
#         fields = ['id','user','order', 'deliveryCrew', 'status', 'total','date','orderItem']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuItem', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'user', 'deliveryCrew', 'status', 'date', 'total', 'orderItems']
