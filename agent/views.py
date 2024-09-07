from rest_framework import viewsets
from rest_framework.response import Response
from .models import Profile, Client, List, Option, Card, Deal
from .serializers import ProfileSerializer, ClientSerializer, ListSerializer, OptionSerializer, CardSerializer, DealSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
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




class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    @action(detail=True, methods=['delete'], url_path='clear-options')
    def clear_options(self, request, pk=None):
        try:
            list_obj = self.get_object()
            options_deleted, _ = Option.objects.filter(list=list_obj).delete()
            return Response({"message": f"{options_deleted} options deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PublicListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        uuid = self.kwargs.get('uuid')
        if uuid:
            queryset = List.objects.filter(uuid=uuid)
            if not queryset.exists():
                raise List('Object with this UUID not found.')
            return queryset
        return List.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        obj = queryset.first()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent']
    search_fields = ['agent', 'client']

    def get_queryset(self):
        queryset = super().get_queryset()
        agent = self.request.query_params.get('agent')
        if agent:
            queryset = queryset.filter(agent=agent)
        return queryset


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
