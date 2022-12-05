# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework import serializers


# Summary class and Summary serializer
class Summary(object):
    def __init__(self, timestamp, resources):
        self.timestamp = timestamp
        self.resources = resources

    def __repr__(self):
        return f"Summary: timestamp: {self.timestamp}, summary: {self.resources}"


class SummarySerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    resources = serializers.DictField()

    def create(self, validated_data):
        return Summary(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get("timestamp", instance.timestamp)
        instance.resources = validated_data.get("resources", instance.resources)
        return instance


# Usage class and Usage serializer
class Usage(object):
    def __init__(self, timestamp, start, end, resources):
        self.timestamp = timestamp
        self.start = start
        self.end = end
        self.resources = resources

    def __repr__(self):
        return f"Usage: timestamp: {self.timestamp}, start: {self.start}, end: {self.end}, resources: {self.resources}"


class UsageSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    resources = serializers.DictField()

    def create(self, validated_data):
        return Usage(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get("timestamp", instance.timestamp)
        instance.start = validated_data.get("start", instance.start)
        instance.end = validated_data.get("end", instance.end)
        instance.resources = validated_data.get("resources", instance.resources)
        return instance


class AllocationUsage(object):
    def __init__(self, name, summary, usages):
        self.name = name
        self.summary = summary
        self.usages = usages

    def __repr__(self):
        return f"AllocationUsage: name: {self.name}, summary: {self.summary}, usage: {self.usages}"


class AllocationUsageSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = SummarySerializer()
    usages = serializers.ListField(child=UsageSerializer())

    def create(self, validated_data):
        usages = []
        for u_data in validated_data["usages"]:
            u = Usage(**u_data)
            usages.append(u)
        validated_data.update({"usages": usages})
        return AllocationUsage(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.summary = validated_data.get("summary", instance.summary)

        usages = []
        for u_data in validated_data["usages"]:
            u = Usage(**u_data)
            usages.append(u)
        validated_data.update({"usages": usages})

        instance.usages = validated_data.get("usages", instance.usages)
        return instance
