from rest_framework import serializers


# Summary class and Summary serializer
class Summary(object):
    def __init__(self, last_update, resources):
        self.last_update = last_update
        self.resources = resources

    def __repr__(self):
        return f"SUMMARY: last update: {self.last_update}, summary: {self.resources}"


class SummarySerializer(serializers.Serializer):
    last_update = serializers.DateTimeField()
    resources = serializers.DictField()

    def create(self, validated_data):
        return Summary(**validated_data)

    def update(self, instance, validated_data):
        instance.last_update = validated_data.get("last_update", instance.last_update)
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
        return f"USAGE: timestamp: {self.timestamp}, start: {self.start}, end: {self.end}, resources: {self.resources}"


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
    def __init__(self, name, summary, usage):
        self.name = name
        self.summary = summary
        self.usage = usage

    def __repr__(self):
        return f"ALLOCATION USAGE: name: {self.name}, summary: {self.summary}, usage: {self.usage}"


class AllocationUsageSerializer(serializers.Serializer):
    name = serializers.CharField()
    summary = SummarySerializer()
    usage = serializers.ListField(child=UsageSerializer())

    def create(self, validated_data):
        usage = []
        for u_data in validated_data["usage"]:
            u = Usage(**u_data)
            usage.append(u)
        validated_data.update({"usage": usage})
        return AllocationUsage(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.summary = validated_data.get("summary", instance.summary)

        usage = []
        for u_data in validated_data["usage"]:
            u = Usage(**u_data)
            usage.append(u)
        validated_data.update({"usage": usage})

        instance.usage = validated_data.get("usage", instance.usage)
        return instance
