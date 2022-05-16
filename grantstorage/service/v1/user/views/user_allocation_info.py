from rest_framework import serializers


class AllocationUsagesResponse(object):
    def __init__(self, allocation_usages):
        self.name = allocation_usages.name
        self.summary = allocation_usages.summary
        self.usage = allocation_usages.usage

    def __str__(self):
        return f"Allocation usages: {self.name}, summary: {self.summary}, usage: {self.usage}"


class AllocationUsagesSerializer(serializers.Serializer):
    name = serializers.CharField
    summary = serializers.DictField()
    usage = serializers.ListField(child=serializers.DictField())