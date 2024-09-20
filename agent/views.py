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
from datetime import timedelta
from django.utils import timezone
from .emails import send_guest_card_email

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent']
    search_fields = ['first_name', 'last_name']



class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['agent']
    search_fields = ['agent', 'client']

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

    def perform_create(self, serializer):
        serializer.save(status='not')

    def perform_update(self, serializer):
        instance = serializer.instance
        status = self.request.data.get('status', instance.status)

        if status == 'pend':
            serializer.save(status='pend')
            serializer.save(invoice_date=timezone.now().date())
            sixty = instance.move_date + timedelta(days=60)
            serializer.save(overdue_date=sixty)

        if status == 'paid':
            serializer.save(status='paid')




class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        card = serializer.save()

        send_guest_card_email(
            agent=card.agent,
            client=card.client,
            property=card.property,
            interested=card.interested,
            move_by=card.move_by
        )
