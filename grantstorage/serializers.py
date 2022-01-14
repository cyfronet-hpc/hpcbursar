from django.contrib.auth.models import User, Group
from rest_framework import serializers
from grantstorage.models import Grant


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant
        exclude = []
