import pymunge
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.apicontroler.v1.apicontroler import UserServicesController
from grantstorage.userinfoservice.user_grant_info import UserGrantInfoResponse, UserGrantInfoSerializer


class MungePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if "Hbtoken" in request.headers and request.method in SAFE_METHODS:
            # hbtoken = request.headers["Hbtoken"]
            # bytes_hbtoken = str.encode(hbtoken)
            # with pymunge.MungeContext() as ctx:
            #     payload, uid, gid = ctx.decode(bytes_hbtoken)
            #     if 'plgmattpokoras' == payload.decode("utf-8"):
            print(request.user)
            return request.user == obj.login

    def has_permission(self, request, view):
        if "Hbtoken" in request.headers:
            hbtoken = request.headers["Hbtoken"]
            bytes_hbtoken = str.encode(hbtoken)
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(bytes_hbtoken)
                if 'plgmattpokoras' == payload.decode("utf-8"):
                    print("fsadfasdfsaf")
        else:
            print(request.headers)
        return True


class UserGrantInfoView(APIView):
    """
        * Requires token authentication.
    """
    #  TODO add authentication
    permission_classes = [MungePermission]

    def get(self, request, login):
        user_service_controller = UserServicesController()
        grants_dict = user_service_controller.user_grant_info(login)
        response = []
        for grant, group in grants_dict.items():
            user_info_model = UserGrantInfoResponse(grant, group)
            user_info_serializer = UserGrantInfoSerializer(user_info_model)
            response.append(user_info_serializer.data)
        return Response(response)
