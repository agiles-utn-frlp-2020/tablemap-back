from django.urls import include, path
from rest_framework import routers

from .views import OrderViewSet, ProductViewSet, TableViewSet, LoginView

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', LoginView.as_view(), name="login")
]
