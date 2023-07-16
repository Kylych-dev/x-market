from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Courier, Collectors
from .serializers import CollectorsSerializer, CourierSerializer


class CourierListAPIView(ListAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class CourierRetrieveAPIView(RetrieveAPIView):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer


class CollectorsListAPIView(ListAPIView):
    queryset = Collectors.objects.all()
    serializer_class = CollectorsSerializer


class CollectorsRetrieveAPIView(RetrieveAPIView):
    queryset = Collectors.objects.all()
    serializer_class = CollectorsSerializer


