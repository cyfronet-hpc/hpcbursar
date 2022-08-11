# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework import serializers


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


# User grant info allocation usage
class UserGrantInfoAllocationUsage(object):
    def __init__(self, allocation_usages):
        self.name = allocation_usages.name
        self.summary = allocation_usages.summary
        self.usage = allocation_usages.usage

    def __str__(self):
        return f"Allocation usages: {self.name}, summary: {self.summary}, usage: {self.usage}"


class UserGrantInfoAllocationUsagesSerializer(serializers.Serializer):
    name = serializers.CharField
    summary = serializers.DictField()
    usage = serializers.ListField(child=serializers.DictField())


# Response
class UserGrantInfoResponse(object):
    def __init__(self, grant, group):
        self.name = grant.name
        self.start = grant.start
        self.end = grant.end
        self.state = grant.status
        self.allocations = [UserGrantInfoAllocation(allocation) for allocation in grant.allocations]
        self.group = grant.group
        self.group_members = group.members + group.leaders
        # self.allocations_usages = allocation_usages

    def __str__(self):
        return f"Grant name: {self.name}, start: {self.start}, end: {self.end}, state: {self.state}, " \
               f"allocations: {self.allocations}, group: {self.group}, group members: {self.group_members}"
        # f"allocation usages: {self.allocations_usages}"


class UserGrantInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    state = serializers.CharField()
    allocations = UserGrantInfoAllocationSerializer(many=True)
    group = serializers.CharField()
    group_members = serializers.ListField(child=serializers.CharField())
    # allocations_usages = UserGrantInfoAllocationUsagesSerializer(many=True)
