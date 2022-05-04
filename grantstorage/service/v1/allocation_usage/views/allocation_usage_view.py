import pymunge
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.service.v1.allocation_usage.controller.allocation_usage_service import AllocationUsageController
from grantstorage.service.v1.allocation_usage.views.allocation_usage_info import AllocationUsageInfoResponse, \
    AllocationUsageInfoResponseSerializer


class AllocationUsageMungePermission(BasePermission):
    def has_permission(self, request, view):
        if "x-auth-hpcbursar" in request.headers:
            encoded_x_hb_auth_token = str.encode(request.headers["x-auth-hpcbursar"])
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(encoded_x_hb_auth_token)
                decoded_payload = payload.decode('utf-8')
                username, service_request = decoded_payload.split(":")
                request_username = request.build_absolute_uri().split('/')[-1]
                if username == request_username:
                    return True
        print("No permission")
        return False


class AllocationUsageInfoView(APIView):
    permission_classes = [AllocationUsageMungePermission]

    # TODO: Implement get method
    def get(self, request, login):
        allocation_usage_controller = AllocationUsageController(login)

        response = []
        return Response(response)
