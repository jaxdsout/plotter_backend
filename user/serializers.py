from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from agent.models import Profile
from agent.serializers import ProfileSerializer

class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_active', )


class UserLoadSerializer(UserSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile')
