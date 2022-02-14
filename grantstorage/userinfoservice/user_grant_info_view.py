import pymunge
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.apicontroler.v1.apicontroler import UserServicesController
from grantstorage.userinfoservice.user_grant_info import UserGrantInfoResponse, UserGrantInfoSerializer


class MungePermission(BasePermission):
    def has_permission(self, request, view):
        print(request.build_absolute_uri())
        if "x-auth-hpcbursar" in request.headers:
            encoded_x_hb_auth_token = str.encode(request.headers["x-auth-hpcbursar"])
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(encoded_x_hb_auth_token)
                print(payload)
                decoded_payload = payload.decode('utf-8')
                username, service_request = decoded_payload.split(":")
                request_username = request.build_absolute_uri().split('/')[-1]
                if username == request_username:
                    return True
        print("No permission")
        return False


class UserGrantInfoView(APIView):
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
