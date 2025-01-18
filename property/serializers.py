from rest_framework import serializers
from .models import Property, Commission


class CommissionSerializer(serializers.ModelSerializer):
    prop_name = serializers.SerializerMethodField()

    class Meta:
        model = Commission
        fields = (
            'id',
            'property',
            'prop_name',
            'send',
            'escort',
            'flat_fee',
            'updated_date',
            'active'
        )

    def create(self, validated_data):
        prop_instance = validated_data.get('property')
        Commission.objects.filter(property=prop_instance, active=True).update(active=False)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('active', False):
            prop_instance = validated_data.get('property', instance.property)
            Commission.objects.filter(property=prop_instance, active=True).exclude(id=instance.id).update(active=False)

        return super().update(instance, validated_data)

    def get_prop_name(self, obj):
        return obj.property.name


class PropertySerializer(serializers.ModelSerializer):
    commission = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'id',
            'name',
            'image',
            'website',
            'market',
            'neighborhood',
            'address',
            'latitude',
            'longitude',
            'email',
            'commission',
        )

    def get_commission(self, obj):
        active_commission = obj.commissions.filter(active=True).first()
        if active_commission:
            class ShortCommissionSerializer(serializers.ModelSerializer):
                class Meta:
                    model = Commission
                    fields = (
                        'id',
                        'send',
                        'escort',
                        'flat_fee',
                        'updated_date',
                        'active'
                    )
            return ShortCommissionSerializer(active_commission).data

        return None

