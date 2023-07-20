from django.urls import path
from .views import ProductListAPIView, ProductRetrieveUpdateDestoyAPIView, ProductCreateAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view()),
    path('<int:pk>/', ProductRetrieveUpdateDestoyAPIView.as_view()),
    path('create/', ProductCreateAPIView.as_view()),
]