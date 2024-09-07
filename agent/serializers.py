from rest_framework import serializers
from .models import Profile, Client, List, Option, Deal, Card
from property.serializers import PropertySerializer


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()


    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_email(self, obj):
        return obj.user.email

    class Meta:
        model = Profile
        fields = (
            'id',
            'trec',
            'user',
            'website',
            'avatar',
            'phone_number',
            'first_name',
            'full_name',
            'email'

        )


class ClientSerializer(serializers.ModelSerializer):
    lists = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'agent',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'lists'
        )

    def get_lists(self, obj):
        return ListSerializer(obj.lists.all(), many=True).data


class ListSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = (
            'id',
            'date',
            'uuid',
            'agent',
            'agent_name',
            'client',
            'client_name',
            'options',
        )

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data

    def get_client_name(self, obj):
        if obj.client:
            return f"{obj.client.first_name} {obj.client.last_name}"
        return None

    def get_agent_name(self, obj):
        if obj.client:
            return f"{obj.agent.first_name} {obj.agent.last_name}"
        return None


class OptionSerializer(serializers.ModelSerializer):
    prop_name = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    website = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'property',
            'prop_name',
            'longitude',
            'latitude',
            'address',
            'website',
            'price',
            'unit_number',
            'layout',
            'sq_ft',
            'available',
            'notes',
            'list'
        )

    def get_prop_name(self, obj):
        return obj.property.name

    def get_longitude(self, obj):
        return obj.property.longitude

    def get_latitude(self, obj):
        return obj.property.latitude

    def get_address(self, obj):
        return obj.property.address

    def get_website(self, obj):
        return obj.property.website


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        fields = (
            'property',
            'unit_no',
            'move_date',
            'lease_term',
            'rent',
            'rate',
            'commission',
            'flat_fee',
            'agent',
            'client'
        )


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'property',
            'agent',
            'client'
        )
