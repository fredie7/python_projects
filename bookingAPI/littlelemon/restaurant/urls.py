# Import dependencies
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# Import security dependency
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

# Define URL routes for the user
router.register(r'users', views.UserViewSet)

# Define URL routes for the bookings
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    # Include all routes registered with the router
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Define routes for the restaurant app's menu views
    path('menu/', views.MenuItemsViewSet.as_view(), name='menu-items'),
    path('menu/<int:pk>/', views.SingleMenuItemViewSet.as_view(), name='single-menu-item'),
    path('restaurant/booking/', include(router.urls)),

    # Incorporate user authentication
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Implement security end-point
    path('api-token-auth/', obtain_auth_token),
]