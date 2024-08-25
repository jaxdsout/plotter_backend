from rest_framework import viewsets
from rest_framework.response import Response
from .models import Profile, Client, List, Option, Card, Deal
from .serializers import ProfileSerializer, ClientSerializer, ListSerializer, OptionSerializer, CardSerializer, DealSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent']
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        agent = self.request.query_params.get('agent')
        if agent:
            queryset = queryset.filter(agent=agent)
        return queryset


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
