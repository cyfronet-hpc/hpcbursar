from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.service.v1.user.controller.userservice import UserServicesController
from grantstorage.service.v1.user.views.permission import UserGrantInfoMungePermission


class UserAllocationInfoView(APIView):
    permission_classes = [UserGrantInfoMungePermission]

    def get(self, request, login):
        user_service_controller = UserServicesController()
        allocations_dict = user_service_controller.user_allocation_info(login)
        response = []
        # TODO: finish implementation here
        return Response
