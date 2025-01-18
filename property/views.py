from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from .models import Property, Commission
from .serializers import PropertySerializer, CommissionSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'id', ]
    search_fields = ['name', 'commissions__active']


class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['property', 'active', ]
    search_fields = ['property__name', ]


