from rest_framework import viewsets
from grantstorage.serializers import UserSerializer, GroupSerializer, GrantSerializer
from grantstorage.models import Grant, User, Group


class UserViewSet(viewsets.ModelViewSet):
    """
        View to list all users in the system.
        * Requires token authentication.
        * Only admin users are able to access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GrantViewSet(viewsets.ModelViewSet):
    """
        View to list all users in the system.

        * Requires token authentication.
        * Only admin users are able to access this view.
    """
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer
