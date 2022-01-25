import pymunge
from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from grantstorage.serializers import UserSerializer, GroupSerializer, GrantSerializer
from grantstorage.models import Grant, User, Group


class MungePermission(BasePermission):
    """
    A base class from which all permission classes should inherit.
    """

    def has_permission(self, request, view):
        if "Hbtoken" in request.headers:
            hbtoken = request.headers["Hbtoken"]
            bytes_hbtoken = str.encode(hbtoken)
            print(bytes_hbtoken)
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(bytes_hbtoken)
                print(payload, uid, gid)
        else:
            print(request.headers)
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class GrantViewSet(viewsets.ModelViewSet):
    """
        View to list all users in the system.

        * Requires token authentication.
        * Only admin users are able to access this view.
    """
    permission_classes = [MungePermission]

    queryset = Grant.objects.all()
    serializer_class = GrantSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        View to list all users in the system.
        * Requires token authentication.
        * Only admin users are able to access this view.
    """
    permission_classes = [MungePermission]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [MungePermission]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
