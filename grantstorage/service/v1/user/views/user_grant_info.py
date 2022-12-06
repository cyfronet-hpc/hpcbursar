# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework import serializers


class UserGrantInfoAllocationUsageSummary(object):
    def __init__(self, summary):
        self.timestamp = summary.timestamp
        self.resources = summary.resources

    def __str__(self):
        return f'AllocationUsageSummary: timestamp: {self.timestamp}, resources: {self.resources}'


class UserGrantInfoAllocationUsageSummarySerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    resources = serializers.DictField()


# User grant info allocation
class UserGrantInfoAllocation(object):
    def __init__(self, allocation):
        self.name = allocation.name
        self.resource = allocation.resource
        self.parameters = allocation.parameters

    def __str__(self):
        return f'Allocation: {self.name}, resource: {self.resource}, parameters: {self.parameters}'


class UserGrantInfoAllocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    resource = serializers.CharField()
    parameters = serializers.DictField()


# # User grant info allocation usage
class UserGrantInfoAllocationUsage(object):
    def __init__(self, allocation_usage):
        self.name = allocation_usage.name
        self.summary = allocation_usage.summary
        # self.usages = allocation_usage.usages

    def __str__(self):
        return f"Allocation usage: {self.name}, summary: {self.summary}"
        # return f"Allocation usage: {self.name}, summary: {self.summary}, usage: {self.usages}"


class UserGrantInfoAllocationUsageSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = UserGrantInfoAllocationUsageSummarySerializer()
    # usages = serializers.ListField(child=serializers.DictField())


# Response
class UserGrantInfoResponse(object):
    def __init__(self, grant, group, allocation_usages):
        self.name = grant.name
        self.start = grant.start
        self.end = grant.end
        self.state = grant.status
        self.allocations = [UserGrantInfoAllocation(allocation) for allocation in grant.allocations]
        self.group = grant.group
        self.group_members = group.members + group.leaders
        self.allocations_usages = [
            UserGrantInfoAllocationUsage(allocation_usage) for allocation_usage in allocation_usages
        ]

    def __str__(self):
        return f"Grant name: {self.name}, start: {self.start}, end: {self.end}, state: {self.state}, " \
               f"allocations: {self.allocations}, group: {self.group}, group members: {self.group_members}", \
               f"allocation usages: {self.allocations_usages}"


class UserGrantInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    state = serializers.CharField()
    allocations = UserGrantInfoAllocationSerializer(many=True)
    group = serializers.CharField()
    group_members = serializers.ListField(child=serializers.CharField())
    allocations_usages = UserGrantInfoAllocationUsageSerializer(many=True)
