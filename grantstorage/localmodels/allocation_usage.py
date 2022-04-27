from rest_framework import serializers


# Summary class and Summary serializer
class Summary(object):
    def __init__(self, summary, last_update):
        self.summary = summary
        self.last_update = last_update

    def __repr__(self):
        return f"SUMMARY: {self.summary}, last update: {self.last_update}"


class SummarySerializer(serializers.Serializer):
    summary = serializers.CharField()
    last_update = serializers.DateField()

    def create(self, validated_data):
        return Summary(**validated_data)

    def update(self, instance, validated_data):
        instance.summary = validated_data.get("summary", instance.summary)
        instance.last_update = validated_data.get("last_update", instance.last_update)
        return instance


# Usage class and Usage serializer
class Usage(object):
    def __init__(self, timestamp, resources):
        self.timestamp = timestamp
        self.resources = resources

    def __repr__(self):
        return f"USAGE: timestamp: {self.timestamp}, resources: {self.resources}"


class UsageSerializer(serializers.Serializer):
    timestamp = serializers.DateField()
    resources = serializers.DictField()

    def create(self, validated_data):
        Usage(**validated_data)

    def update(self, instance, validated_data):
        instance.timestamp = validated_data.get("timestamp", instance.timestamp)
        instance.resources = validated_data.get("resources", instance.resources)
        return instance


# Allocation class and Allocation serializer
class AllocationUsage:
    def __init__(self, name, summary, usage):
        self.name = name
        self.summary = summary
        self.usage = usage

    def __str__(self):
        return f"ALLOCATION USAGE: name: {self.name}, summary: {self.summary}, usage: {self.usage}"


class AllocationUsageSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = serializers.DictField()
    usage = serializers.ListField(child=serializers.DictField())

    def create(self, validated_data):
        # handling summary and usage
        summary, usage = self.handle_summary_and_usage(validated_data)

        validated_data.update({"summary": summary, "usage": usage})
        return AllocationUsage(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        # handling summary and usage
        summary, usage = self.handle_summary_and_usage(validated_data)

        validated_data.update({"summary": summary, "usage": usage})
        instance.summary = validated_data.get("summary", instance.summary)
        instance.usage = validated_data.get("usage", instance.usage)
        return instance

    @staticmethod
    def handle_summary_and_usage(validated_data):
        # handling summary
        summary = []
        for sum_data in validated_data["summary"]:
            summary.append(Summary(**sum_data))

        # handling usage
        usage = []
        for usage_data in validated_data["usage"]:
            usage.append(Usage(**usage_data))

        return summary, usage
