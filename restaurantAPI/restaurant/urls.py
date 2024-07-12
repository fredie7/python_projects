from django.urls import path
from . import views

# urlpatterns = [
#     path('groups/manager/users', views.GroupViewSet.as_view(
#         {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
#     path('categories', views.CategoriesView.as_view()),
#     path('menu-items', views.MenuItemsView.as_view()),
#     path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
#     path('cart/menu-items', views.CartView.as_view()),
#     path('cart/menu-items', views.CartView.as_view()),
#     path('orders', views.OrderView.as_view()),
#     path('orders/<int:pk>', views.SingleOrderView.as_view()),
#     path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
#         {'get': 'list', 'post': 'create', 'delete': 'destroy'}))
# ]

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('groups/manager/users', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='group-list'),
    path('categories', views.CategoriesView.as_view(), name='category-list'),
    path('menu-items', views.MenuItemsView.as_view(), name='menuitem-list'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='menuitem-detail'),
    path('cart/menu-items', views.CartView.as_view(), name='cart-list'),
    path('orders', views.OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='order-detail'),
    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='deliverycrew-list')
]
