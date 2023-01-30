# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController
from .admin_permission import AdminPermission


class AdminAllocationInfo(object):
    def __init__(self, allocation):
        self.name = allocation.name
        self.resource = allocation.resource
        self.parameters = allocation.parameters


class AdminAllocationInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    resource = serializers.CharField()
    parameters = serializers.DictField()


class AdminGrantInfo(object):
    def __init__(self, grant):
        self.name = grant.name
        self.group = grant.group
        self.status = grant.status
        self.start = grant.start
        self.end = grant.end
        self.allocations = [AdminAllocationInfo(allocation) for allocation in grant.allocations]


class AdminGrantInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    group = serializers.CharField()
    status = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    allocations = AdminAllocationInfoSerializer(many=True)


class AdminGrantsInfoView(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, name):
        admin_service_controller = AdminServicesController()
        grant = admin_service_controller.grant_info(name)
        grant_info = AdminGrantInfo(grant)
        response = AdminGrantInfoSerializer(grant_info)
        return Response(response.data)
