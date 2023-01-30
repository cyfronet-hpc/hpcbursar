# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController
from .admin_permission import AdminPermission


class AdminSummaryInfo(object):
    def __init__(self, summary):
        self.timestamp = summary.timestamp
        self.resources = summary.resources


class AdminSummaryInfoSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    resources = serializers.DictField()


class AdminUsageInfo(object):
    def __init__(self, usage):
        self.timestamp = usage.timestamp
        self.start = usage.start
        self.end = usage.end
        self.resources = usage.resources


class AdminUsageInfoSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    resources = serializers.DictField()


class AdminAllocationUsageInfo(object):
    def __init__(self, allocation_usage):
        self.name = allocation_usage.name
        self.summary = AdminSummaryInfo(allocation_usage.summary)
        self.usages = [AdminUsageInfo(usage) for usage in allocation_usage.usages]


class AdminAllocationUsageInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = AdminSummaryInfoSerializer
    usages = serializers.ListField(child=AdminUsageInfoSerializer())


class AdminAllocationsInfoView(APIView):
    permission_classes = [AdminPermission]

    def get(self, request, name):
        admin_service_controller = AdminServicesController()
        allocation_usage = admin_service_controller.allocation_usage_info(name)
        allocation_usage_info = AdminAllocationUsageInfo(allocation_usage)
        response = AdminAllocationUsageInfoSerializer(allocation_usage_info)
        return Response(response.data)
