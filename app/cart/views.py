from rest_framework.views import APIView
from rest_framework.response import Response

from ..product import models
from .cart import Cart
from ..product import serializers
from django.shortcuts import get_object_or_404


# операций с корзиной

class CartAddView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(models.Product, id=product_id)
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            cart.add(product=product,
                     quantity=serializer.validated_data['quantity'],
                     override_quantity=serializer.validated_data['override'])
            return Response({'success': True})
        else:
            return Response(serializer.errors, status=400)
    
class CartRemoveView(APIView):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(models.Product, id=product_id)
        cart.remove(product)
        return Response({'success': True})
    
class CartDetailView(APIView):
    def get(self, request):
        cart = Cart(request)
        serializer = serializers.ProductSerializer(cart, many=True)
        return Response(serializer.data)