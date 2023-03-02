# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController
from .admin_permission import AdminPermission


class AdminGroupInfo(object):
    def __init__(self, group):
        self.name = group.name
        self.status = group.status
        self.members = group.members
        self.leaders = group.leaders


class AdminGroupInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField())
    leaders = serializers.ListField(child=serializers.CharField())


class AdminGroupsInfo(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, name):
        admin_service_controller = AdminServicesController()
        group = admin_service_controller.group_info(name)
        group_info = AdminGroupInfo(group)
        response = AdminGroupInfoSerializer(group_info)
        return Response(response.data)
