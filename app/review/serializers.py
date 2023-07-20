from rest_framework import serializers
from .models import ProductReview, CourierReview, ReplyOnProductReview


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('rating', 'comment')


class CourierReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierReview
        fields = ('rating', 'comment')


class ListProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = (
            'author',
            'comment',
            "rating",
            'created_at',
            'updated_at'
        )


class ListCourierReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = (
            'author',
            'comment',
            "rating",
            'created_at',
            'updated_at'
        )


class ReplyOnProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyOnProductReview
        fields = ('comment',)


class ReplyOnProductReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyOnProductReview
        fields = '__all__'
