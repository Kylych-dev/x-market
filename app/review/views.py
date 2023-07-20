from rest_framework import generics, viewsets, mixins
from .serializers import (
    ProductReviewSerializer,
    CourierReviewSerializer,
    ListProductReviewSerializer,
    ListCourierReviewSerializer,
    ReplyOnProductReviewSerializer,
    ReplyOnProductReviewListSerializer,

)
from .models import ProductReview, Product, CourierReview, ReplyOnProductReview
from django.contrib.auth.models import User


class CreateAndListProductReview(generics.ListCreateAPIView):
    queryset = ProductReview.objects.all()

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                return ProductReviewSerializer
            case "GET":
                return ListProductReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        product = Product.objects.get(pk=pk)
        serializer.save(product=product)
        # serializer.save(product=product, author=self.request.user)


class ReviewOnProductViewSet(mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = ProductReviewSerializer
    queryset = ProductReview.objects.all()


class CreateCourierReview(generics.ListCreateAPIView):
    serializer_class = CourierReviewSerializer
    queryset = CourierReview.objects.all()

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                return CourierReviewSerializer
            case "GET":
                return ListCourierReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        courier = User.objects.get(pk=pk)
        serializer.save(courier=courier)
        # serializer.save(product=product, author=self.request.user)


class ReviewOnCourierViewSet(mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = CourierReviewSerializer
    queryset = CourierReview.objects.all()


class ReplyOnProductReviewView(generics.ListCreateAPIView):
    serializer_class = ReplyOnProductReviewSerializer
    queryset = ReplyOnProductReview.objects.all()

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                return ReplyOnProductReviewSerializer
            case "GET":
                return ReplyOnProductReviewListSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        review = ProductReview.objects.get(pk=pk)
        serializer.save(review=review)
