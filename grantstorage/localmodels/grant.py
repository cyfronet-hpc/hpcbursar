from rest_framework import serializers


class Allocation(object):
    def __init__(self, name, resource, parameters):
        self.name = name
        self.resource = resource
        self.parameters = parameters

    def __repr__(self):
        return f'Allocation: {self.name}, resource: {self.resource}, parameters: {self.parameters}'


class AllocationSerializer(serializers.Serializer):
    name = serializers.CharField()
    resource = serializers.CharField()
    parameters = serializers.DictField()


class Grant(object):
    def __init__(self, name, group, status, start, end, allocations):
        self.name = name
        self.group = group
        self.status = status
        self.start = start
        self.end = end
        self.allocations = allocations

    def __str__(self):
        return f'Grant: {self.name}, group: {self.group}, status: {self.status}, start: {self.start}, end: {self.end}, ' \
               f'allocations: {self.allocations}'


class GrantSerializer(serializers.Serializer):
    name = serializers.CharField()
    group = serializers.CharField()
    status = serializers.CharField()
    start = serializers.DateField
    end = serializers.DateField()
    allocations = AllocationSerializer(many=True)
