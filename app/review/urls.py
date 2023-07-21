from django.urls import path, include
from rest_framework import routers
from .views import (CreateAndListProductReview,
                    ReviewOnProductViewSet,
                    CreateCourierReview,
                    ReviewOnCourierViewSet,
                    ReplyOnProductReviewView
                    )

router = routers.DefaultRouter()
router.register(r'product-review-details', ReviewOnProductViewSet, basename='product-review-details')
router.register(r'courier-review-details', ReviewOnCourierViewSet, basename='courier-review-details')

urlpatterns = [path('product-review/<int:pk>/', CreateAndListProductReview.as_view(), name='product-review'),
               path('courier-review/<int:pk>/', CreateCourierReview.as_view(), name='courier-review'),
               path('reply-on-product/<int:pk>/', ReplyOnProductReviewView.as_view(), name='reply'),
               path('', include(router.urls))]
