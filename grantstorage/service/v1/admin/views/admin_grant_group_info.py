import pymunge
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from django.conf import settings

from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController


class AdminGrantInfoAllocation(object):
    def __init__(self, allocation):
        self.name = allocation.name
        self.resource = allocation.resource
        self.parameters = allocation.parameters


class AdminGrantInfoAllocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    resource = serializers.CharField()
    parameters = serializers.DictField()


class AdminGrantInfoGrant(object):
    def __init__(self, grant):
        self.name = grant.name
        self.start = grant.start
        self.end = grant.end
        self.state = grant.status
        self.allocations = [AdminGrantInfoAllocation(allocation) for allocation in grant.allocations]
        self.group = grant.group


class AdminGrantInfoGrantSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    state = serializers.CharField()
    allocations = AdminGrantInfoAllocationSerializer(many=True)
    group = serializers.CharField()


class AdminGrantInfoGroup(object):
    def __init__(self, group):
        self.name = group.name
        self.members = group.members
        self.leaders = group.leaders


class AdminGrantInfoGroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField())
    leaders = serializers.ListField(child=serializers.CharField())


class AdminGrantInfoResponse(object):
    def __init__(self, grants, groups):
        self.grants = [AdminGrantInfoGrant(grant) for grant in grants]
        self.groups = [AdminGrantInfoGroup(group) for group in groups]


class AdminGrantInfoReponseSerializer(serializers.Serializer):
    grants = AdminGrantInfoGrantSerializer(many=True)
    groups = AdminGrantInfoGroupSerializer(many=True)


class AdminMungePermission(BasePermission):
    def has_permission(self, request, view):
        if "x-auth-hpcbursar" in request.headers:
            encoded_x_hb_auth_token = str.encode(request.headers["x-auth-hpcbursar"])
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(encoded_x_hb_auth_token)
                decoded_payload = payload.decode('utf-8')
                username, service_request = decoded_payload.split(":")
                request_username = request.build_absolute_uri().split('/')[-1]
                if username == settings.SLURM_ADMIN_USER:
                    return True
        return False


class AdminGrantGroupInfoView(APIView):
    permission_classes = [AdminMungePermission]

    def get(self, request):
        admin_service_controller = AdminServicesController()
        grants, groups = admin_service_controller.grant_group_info()
        grant_group_info = AdminGrantInfoResponse(grants, groups)
        response = AdminGrantInfoReponseSerializer(grant_group_info)
        return Response(response.data)
