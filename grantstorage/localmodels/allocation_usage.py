from rest_framework import serializers


# Summary class and Summary serializer
class Summary(object):
    def __init__(self, summary, last_update):
        self.summary = summary
        self.last_update = last_update

    def __repr__(self):
        return f"SUMMARY: summary: {self.summary}, last update: {self.last_update}"


class SummarySerializer(serializers.Serializer):
    summary = serializers.CharField()
    last_update = serializers.DateTimeField()

    def create(self, validated_data):
        return Summary(**validated_data)

    def update(self, instance, validated_data):
        instance.summary = validated_data.get("summary", instance.summary)
        instance.last_update = validated_data.get("last_update", instance.last_update)
        return instance


# Usage class and Usage serializer
class Usage(object):
    def __init__(self, usage):
        self.usage = usage

    def __repr__(self):
        return f"USAGE: usage: {self.usage}"


class UsageSerializer(serializers.Serializer):
    usage = serializers.ListField(child=serializers.DictField())

    def create(self, validated_data):
        return Usage(**validated_data)

    def update(self, instance, validated_data):
        instance.usage = validated_data.get("usage", instance.usage)
        return instance


class AllocationUsage(object):
    def __init__(self, name, summary, usage):
        self.name = name
        self.summary = summary
        self.usage = usage

    def __repr__(self):
        return f"ALLOCATION USAGE: name: {self.name}, summary: {self.summary}, usage: {self.usage}"


class AllocationUsageSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = SummarySerializer()
    usage = UsageSerializer()

    def create(self, validated_data):
        return AllocationUsage(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data("name", instance.name)
        instance.summary = validated_data.get("summary", instance.summary)
        instance.usage = validated_data("usage", instance.usage)
        return instance
