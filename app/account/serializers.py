from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Collectors, Courier


class CollectorsDetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collectors
        fields = ('img',
                  'full_name',
                  'languages',
                  'date_of_birth',
                  'phone_number',
                  'home_address',
                  'email'
                  )


class CollectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collectors
        fields = (
            'full_name',
            'email',
        )


class CourierDetailsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('img',
                  'full_name',
                  'languages',
                  'date_of_birth',
                  'phone_number',
                  'home_address',
                  'email'
                  )


class CourierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'full_name',
            'email',
        )
