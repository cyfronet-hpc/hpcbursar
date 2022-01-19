from rest_framework import serializers
from grantstorage.models import Grant, User, Group


class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant
        exclude = []


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = []


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        exclude = []
