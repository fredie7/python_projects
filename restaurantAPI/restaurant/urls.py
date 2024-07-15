# Import dependencies

from django.urls import path
from . import views

urlpatterns = [
    # URL for manager group operations list, create, delete users
    path('groups/manager/users', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='group-list'),
    
    # URL for listing and creating categories
    path('categories', views.CategoriesView.as_view(), name='category-list'),

    # URL for listing and creating menu items
    path('menu-items', views.MenuItemsView.as_view(), name='menuitem-list'),

    # URL for retrieving, updating, and deleting a single menu item
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menuitem-detail'),

    # URL for listing and creating cart items
    path('cart/menu-items', views.CartView.as_view(), name='cart-list'),

    # URL for listing and creating orders
    path('orders', views.OrderView.as_view(), name='order-list'),

    # URL for retrieving and updating a single order
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='order-detail'),

    # URL  for delivery crew group operations -list, create, delete users
    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='deliverycrew-list')
]
