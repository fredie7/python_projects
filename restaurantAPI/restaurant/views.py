from django.shortcuts import render
from .serializers import CartItemSerializer, MenuItemSerializer, UserSerializer, CategorySerializer, OrderItemSerializer, OrderSerializer
from .models import Category, MenuItem, Cart, Order, OrderItem
from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from datetime import date
from rest_framework import viewsets

# # Admin view:
class GroupViewSet(viewsets.ViewSet):
    def list(self, request):
        managers = User.objects.all().filter(groups__name = 'Manager')
        users = UserSerializer(managers, many=True)
        return Response(users.data)
    
    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        print(user)
        return Response({"message": "user added to the managers group"}, 200)
    
    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

# # Categories view:
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permitted = []
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]

        return [permission() for permission in permitted]

# # Whole Menu view:
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title']
    ordering_fields = ['price', 'inventory']

    def get_permissions(self):
        permitted = []
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]

        return [permission() for permission in permitted]

# # Single item's view:    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permitted = []
        if self.request.method != 'GET':
            permitted = [IsAuthenticated]
        return [permission() for permission in permitted]
    
# Cart view
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")
# Order view
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count() == 0:
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.all().filter(deliveryCrew=self.request.user)
        else:
            return Order.objects.all()

    def create(self, request, *args, **kwargs):
        menuItem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuItem_count == 0:
            return Response({"message": "no item in cart"}, status=400)

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id

        order_serializer = OrderSerializer(data=data)
        if order_serializer.is_valid():
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()
            for item in items:
                orderitem = OrderItem(
                    order=order,
                    menuItem=item.menuItem,
                    price=item.price,
                    quantity=item.quantity,
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(result, status=201)
        else:
            return Response(order_serializer.errors, status=400)

    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items:
            total += item.price
        return total
    
class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Normal user, not belonging to any group = Customer
            return Response('Not Ok')
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)

class DeliveryCrewViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery crew')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == True:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        delivery_crew = Group.objects.get(name="Delivery crew")
        delivery_crew.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == True:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        delivery_crew = Group.objects.get(name="Delivery crew")
        delivery_crew.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)