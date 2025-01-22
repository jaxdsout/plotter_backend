from rest_framework import viewsets
from rest_framework.response import Response
from .models import Profile, Client, List, Option, Card, Deal
from .serializers import ProfileSerializer, ClientSerializer, ListSerializer, OptionSerializer, CardSerializer, DealSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from datetime import timedelta
from django.utils import timezone
from .emails import send_guest_card_email

from rest_framework.exceptions import ValidationError

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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['agent']
    search_fields = ['first_name', 'last_name']


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['agent']

    @action(detail=True, methods=['delete'], url_path='clear-options')
    def clear_options(self, request, pk=None):
        try:
            list_obj = self.get_object()
            options_deleted, _ = Option.objects.filter(list=list_obj).delete()
            return Response({"message": f"{options_deleted} options deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update-options')
    def update_options(self, request, pk=None):
        try:
            list_obj = self.get_object()

            options_data = request.data.get('options', [])
            if not isinstance(options_data, list):
                raise ValidationError({"options": "Expected a list of options."})

            # Process each option in the list
            for idx, option_data in enumerate(options_data):
                option_id = option_data.get('id')
                if option_id is None:
                    raise ValidationError({"options": f"Option at index {idx} is missing an ID."})

                # Update the option's order and other fields if provided
                Option.objects.filter(id=option_id, list=list_obj).update(
                    order=idx,
                    price=option_data.get('price', None),
                    unit_number=option_data.get('unit_number', None),
                    layout=option_data.get('layout', None),
                    sq_ft=option_data.get('sq_ft', None),
                    available=option_data.get('available', None),
                    notes=option_data.get('notes', None),
                )

            return Response({'status': 'success', 'message': f'{len(options_data)} options updated.'},
                            status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'status': 'error', 'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['list']


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['agent']

    def perform_create(self, serializer):
        serializer.save(status='not')

    def perform_update(self, serializer):
        instance = serializer.instance
        status = self.request.data.get('status', instance.status)

        if status == 'pend':
            instance.status = 'pend'
            instance.invoice_date = timezone.now().date()
            if instance.move_date:
                instance.overdue_date = instance.move_date + timedelta(days=60)
        elif status == 'paid':
            instance.status = 'paid'

        serializer.save()

# class DealViewSet(viewsets.ModelViewSet):
#     queryset = Deal.objects.all()
#     serializer_class = DealSerializer
#     filter_backends = [DjangoFilterBackend,]
#     filterset_fields = ['agent']
#
#     def perform_create(self, serializer):
#         serializer.save(status='not')
#
#     def perform_update(self, serializer):
#         instance = serializer.instance
#         status = self.request.data.get('status', instance.status)
#
#         if status == 'pend':
#             serializer.save(status='pend')
#             serializer.save(invoice_date=timezone.now().date())
#             sixty = instance.move_date + timedelta(days=60)
#             serializer.save(overdue_date=sixty)
#
#         if status == 'paid':
#             serializer.save(status='paid')


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
