from django.urls import path
from rest_framework import routers
from .views import CollectorsInfoAPIView, CourierInfoAPIView


router = routers.DefaultRouter()
router.register(r'api-collector/', CollectorsInfoAPIView, basename='api-collector')
router.register(r'api-courier/', CourierInfoAPIView, basename='api-courier')

urlpatterns = [
    
]