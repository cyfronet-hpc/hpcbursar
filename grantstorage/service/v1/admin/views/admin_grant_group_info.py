# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController
from grantstorage.service.v1.admin.views.admin_grant_group_info_permission import AdminMungePermission


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
        self.status = grant.status
        self.allocations = [AdminGrantInfoAllocation(allocation) for allocation in grant.allocations]
        self.group = grant.group


class AdminGrantInfoGrantSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    status = serializers.CharField()
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


class AdminGrantGroupInfoView(APIView):
    permission_classes = [AdminMungePermission]

    def get(self, request):
        admin_service_controller = AdminServicesController()
        grants, groups = admin_service_controller.grant_group_info()
        grant_group_info = AdminGrantInfoResponse(grants, groups)
        response = AdminGrantInfoReponseSerializer(grant_group_info)
        return Response(response.data)
