from rest_framework import serializers
from . import models


"""
class OrderedFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderedFood
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    ordered_food = OrderedFoodSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
"""


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
        