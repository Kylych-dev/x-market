from rest_framework import serializers

# from django.contrib.auth.models import User

from .models import Product
from ..category.models import Category
 
from ..account.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'sell_price', 'capacity',
                  'is_favorite', 'owner', 'category', 'image']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['category'] = CategorySerializer(instance.category).data['name']
        ret['owner'] = UserSerializers(instance.owner).data
        ret['is_favorite'] = UserSerializers(instance.owner).data
        return ret
