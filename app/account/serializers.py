from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Collectors, Courier

class CollectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collectors
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'