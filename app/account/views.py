from rest_framework import viewsets
from .models import Courier, Collectors
from .serializers import (CollectorsDetailInfoSerializer,
                          CourierDetailsInfoSerializer,
                          CollectorListSerializer,
                          CourierListSerializer)


class CourierInfoAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Courier.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CourierListSerializer
        return CourierDetailsInfoSerializer


class CollectorsInfoAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Collectors.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CollectorListSerializer
        return CollectorsDetailInfoSerializer
