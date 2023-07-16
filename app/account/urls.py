from django.urls import path
from .views import CollectorsListAPIView, CollectorsRetrieveAPIView, CourierListAPIView, CourierRetrieveAPIView

urlpatterns = [
    path('api-collectors/', CollectorsListAPIView.as_view()),
    path('<int:pk>/', CollectorsRetrieveAPIView.as_view()),
    path('api-courier/', CourierListAPIView.as_view()),
    path('<int:pk>/', CourierRetrieveAPIView.as_view())
]