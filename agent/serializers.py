from rest_framework import serializers
from .models import Profile, Client, List, Option
from property.serializers import PropertyNameSerializer


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_first_name(self, obj):
        return obj.user.first_name

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
            'full_name'

        )


class ClientSerializer(serializers.ModelSerializer):
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


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = (
            'id',
            'date',
            'agent',
            'client',
            'options'
        )


class OptionSerializer(serializers.ModelSerializer):
    prop_name = serializers.SerializerMethodField()
    def get_prop_name(self, obj):
        return obj.property.name

    class Meta:
        model = Option
        fields = (
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