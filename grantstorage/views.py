import pymunge
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.apicontroler.v1.apicontroler import UserServicesController
from grantstorage.models import UserGrantInfoResponse


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


class UserServicesView(APIView):
    """
        * Requires token authentication.
        * Only admin users are able to access this view.
    """

    # TODO add authentication
    def get(self, request, login):
        user_service_controller = UserServicesController()
        grants_dict = user_service_controller.user_grant_info(login)
        response = []
        for grant, group in grants_dict.items():
            response.append(UserGrantInfoResponse(grant, group))
        return Response(response)
