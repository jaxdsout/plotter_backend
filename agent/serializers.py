from rest_framework import serializers
from .models import Agent, Client, List, Option


class AgentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = (
            'trec_id',
            'user',
            'full_name',
            'first_name'
        )

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_first_name(self, obj):
        return obj.user.first_name


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'agent',
            'lists'
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = (
            'id',
            'creation',
            'agent',
            'client',
            'options'
        )


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = (
            'property',
            'price',
            'unit_number',
            'layout',
            'sq_ft',
            'date_available',
            'notes_specials',
            'list'
        )