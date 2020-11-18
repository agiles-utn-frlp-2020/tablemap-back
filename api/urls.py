from django.urls import include, path
from rest_framework import routers

from .views import (LoginView, LogoutView, OrderViewSet, ProductOrderViewSet,
                    ProductViewSet, TableViewSet)

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'product-order', ProductOrderViewSet, basename='product-order')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', LoginView.as_view(), name="login"),
    path('v1/logout/', LogoutView.as_view(), name="logout")
]
