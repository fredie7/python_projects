# Import dependencies

from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from datetime import date
from rest_framework import viewsets

# Import serializers and models

from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CartItemSerializer, MenuItemSerializer, UserSerializer, CategorySerializer, OrderItemSerializer, OrderSerializer

# Admin view to handle manager group-related actions
class GroupViewSet(viewsets.ViewSet):

    # List all users in the 'Manager' group
    def list(self, request):

        # Retrieve all users belonging to the 'Manager' group
        managers = User.objects.all().filter(groups__name = 'Manager')

        # Serialize the user data
        users = UserSerializer(managers, many=True)

        # Return the serialized data as a response
        return Response(users.data)
    
    # Add a user to the 'Manager' group
    def create(self, request):

        # Get the user object based on the provided username or return 404
        user = get_object_or_404(User, username=request.data['username'])

        # Get the 'Manager' group object
        managers = Group.objects.get(name="Manager")

         # Add the user to the 'Manager' group
        managers.user_set.add(user)
    
        return Response({"message": "user added to the managers group"}, 200)
    
    # Remove a user from the 'Manager' group
    def destroy(self, request):

        # Get the user object based on the provided username or return a 'not found'/ 404
        user = get_object_or_404(User, username=request.data['username'])

        # Get the 'Manager' group object
        managers = Group.objects.get(name="Manager")

        # Remove the user from the 'Manager' group
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

#List and create categories
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Define permissions
    def get_permissions(self):
        permitted = []

        # Allow only authenticated users to create categories
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]
        
        # Return the list of permissions
        return [permission() for permission in permitted]

#List and create menu items with search and ordering properties
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # Enable search by category title
    search_fields = ['category__title']

    # Enable ordering by price and inventory
    ordering_fields = ['price', 'inventory']

    # Define permissions
    def get_permissions(self):
        permitted = []

        # Allow only authenticated users to create menu items
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]

        # Return a list of permissions
        return [permission() for permission in permitted]

# Retrieve, update, and delete a specific menu item    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    # Define permissions
    def get_permissions(self):
        permitted = []
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]
        return [permission() for permission in permitted]
    
# List and create cart items, and delete all items for the current user
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemSerializer

    # Ensure the user is authenticated
    permission_classes = [IsAuthenticated]

    # Override the default queryset to filter by the current user
    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
    
    # Delete all items from the current user's cart
    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")

# List and create orders
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    # Override the default queryset based on user roles
    def get_queryset(self):
        
        # Enable superuser to see all orders
        if self.request.user.is_superuser:
            return Order.objects.all()
        
        # Enable normal user to see only their own orders
        elif self.request.user.groups.count() == 0:
            return Order.objects.all().filter(user=self.request.user)
        
        # Enable delivery crew to see orders assigned to them
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.all().filter(deliveryCrew=self.request.user)
        
        # Managers to see all orders
        else:
            return Order.objects.all()
    
    # Create a new order
    def create(self, request, *args, **kwargs):

        # Confirm that the cart is empty
        menuItem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuItem_count == 0:
            return Response({"message": "no item in cart"}, status=400)

        # Copy request data and calculate total price
        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id

        # Serialize the order data
        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            # Transfer items from cart to order
            items = Cart.objects.all().filter(user=self.request.user).all()
            for item in items:
                orderitem = OrderItem(
                    order=order,
                    menuItem=item.menuItem,
                    price=item.price,
                    quantity=item.quantity,
                )
                orderitem.save()
            
            # Clear the cart
            Cart.objects.all().filter(user=self.request.user).delete()

            # Return the created order data
            result = order_serializer.data.copy()
            result['total'] = total
            return Response(result, status=201)
        else:
            return Response(order_serializer.errors, status=400)
    
    # Sum up the total price of items in the cart
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items:
            total += item.price
        return total

# Retrieve and update a specific order
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    # Ensure the current user is authenticated
    permission_classes = [IsAuthenticated]

    # Override the update method to restrict updates by customers
    def update(self, request, *args, **kwargs):
        
        # Normal user, not belonging to any group is considerd a Customer, and not allowed to carry out this action
        if self.request.user.groups.count()==0:
            return Response('Not Ok')
        
        #Everyone else (Super Admin, Manager and Delivery Crew) is allowed to carry out this action
        else:
            return super().update(request, *args, **kwargs)

# Handle delivery crew group-related actions
class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # List all users in the 'Delivery crew' group
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery crew')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    # Add a user to the 'Delivery crew' group
    def create(self, request):
        
        #only for super admin and managers are allowed to carry out this action
        if self.request.user.is_superuser == True:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        # Get the user object based on the provided username or return 'Not Found'/404
        user = get_object_or_404(User, username=request.data['username'])

        # Get the 'Delivery crew' group object
        delivery_crew = Group.objects.get(name="Delivery crew")

        # Add user to the 'Delivery crew' group
        delivery_crew.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)
    
    # Remove a user from the 'Delivery crew' group
    def destroy(self, request):
        
        #only super admin and managers are allowed to carry out this action
        if self.request.user.is_superuser == True:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
            
        # Get the user object based on the provided username or return 'Not Fount'/404
        user = get_object_or_404(User, username=request.data['username'])

        # Get the 'Delivery crew' group object
        delivery_crew = Group.objects.get(name="Delivery crew")

        # Remove the user from the 'Delivery crew' group
        delivery_crew.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)