from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.service.v1.user.controller.userservice import UserServicesController
from grantstorage.service.v1.user.views.user_grant_info import UserGrantInfoResponse, UserGrantInfoSerializer
from grantstorage.service.v1.user.views.permission import UserGrantInfoMungePermission


class UserGrantInfoView(APIView):
    permission_classes = [UserGrantInfoMungePermission]

    def get(self, request, login):
        user_service_controller = UserServicesController()
        grants_dict = user_service_controller.user_grant_info(login)
        # allocation_usages_dict = user_service_controller.user_allocation_info(login)
        response = []
        for grant, group in grants_dict.items():
            # allocation_usage = ["a", "b", "c"]
            user_info_model = UserGrantInfoResponse(grant, group)
            user_info_serializer = UserGrantInfoSerializer(user_info_model)
            response.append(user_info_serializer.data)
        return Response(response)
