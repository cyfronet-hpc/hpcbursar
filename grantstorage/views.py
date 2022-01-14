from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from grantstorage.serializers import UserSerializer, GroupSerializer, GrantSerializer
from grantstorage.models import Grant


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GrantViewSet(viewsets.ModelViewSet):
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer
