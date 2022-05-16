from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.service.v1.user.controller.userservice import UserServicesController
from grantstorage.service.v1.user.views.permission import UserGrantInfoMungePermission
from grantstorage.service.v1.user.views.user_allocation_info import AllocationUsagesResponse, AllocationUsagesSerializer


class UserAllocationInfoView(APIView):
    permission_classes = [UserGrantInfoMungePermission]

    def get(self, request, login):
        user_service_controller = UserServicesController()
        allocation_usages_dict = user_service_controller.user_allocation_info(login)
        response = []
        for allocation in allocation_usages_dict:
            allocation_usage_model = AllocationUsagesResponse(allocation)
            allocation_usage_serializer = AllocationUsagesSerializer(allocation_usage_model)
            response.append(allocation_usage_serializer.data)
        return Response(response)
