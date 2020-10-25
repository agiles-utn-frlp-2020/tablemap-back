from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet, TableViewSet

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'tables', TableViewSet, basename='tables')

urlpatterns = [
    path('v1/', include(router.urls)),
    #  path('apis/', include('rest_framework.urls', namespace='rest_framework'))

]
