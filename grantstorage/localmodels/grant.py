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

    def create(self, validated_data):
        return Allocation(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.resource = validated_data.get('resource', instance.name)
        instance.parameters = validated_data.get('parameters', instance.name)
        return instance


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
    start = serializers.DateField()
    end = serializers.DateField()
    allocations = AllocationSerializer(many=True)

    def create(self, validated_data):
        # properly handle allocations as nested list
        allocations = []
        for allocation_data in validated_data['allocations']:
            allocation = Allocation(**allocation_data)
            allocations += [allocation]
        validated_data.update({'allocations': allocations})
        return Grant(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.group = validated_data.get('group', instance.group)
        instance.status = validated_data.get('status', instance.status)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)

        # properly handle allocations as nested list
        allocations = []
        for allocation_data in validated_data['allocations']:
            allocation = Allocation(**allocation_data)
            allocations += [allocation]
        validated_data.update({'allocations': allocations})

        instance.allocations = validated_data.get('allocations', instance.allocations)
        return instance
