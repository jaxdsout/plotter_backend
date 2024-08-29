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
            'first_name',
            'last_name',
            'email',
            'agent',
            'phone_number',
            'lists'
        )

    def get_lists(self, obj):
        return ListSerializer(obj.lists.all(), many=True).data


class ListSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = (
            'id',
            'date',
            'agent',
            'client',
            'options',
            'full_name'
        )

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data

    def get_full_name(self, obj):
        if obj.client:
            return f"{obj.client.first_name} {obj.client.last_name}"
        return None


class OptionSerializer(serializers.ModelSerializer):
    prop_name = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = (
            'id',
            'property',
            'prop_name',
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


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        fields = (
            'property',
            'rent',
            'rate',
            'commission',
            'flat_fee',
            'move_date',
            'unit_no',
            'lease_term',
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
