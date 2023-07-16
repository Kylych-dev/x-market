from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product
from ..category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        ret =  super().to_representation(instance)
        ret['category'] = CategorySerializer(instance.category).data['name']
        ret['owner'] = UserSerializers(instance.owner).data  
        return ret
    
    