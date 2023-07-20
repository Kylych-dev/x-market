from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['post'], detail=True)
    def make_payment(self, request, pk=None):
        order = self.get_object()
        # Ваш код обработки оплаты

        # Возвращаем статус успешной оплаты или другие данные
        return Response({"message": "Payment successful!"})
