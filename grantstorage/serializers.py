from rest_framework import serializers


class UserInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    state = serializers.CharField()
    allocations = serializers.ListField(child=serializers.CharField())
    group = serializers.CharField()
    group_members = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return Grant(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.start = validated_data.get("start", instance.start)
        instance.end = validated_data.get("end", instance.end)
        instance.state = validated_data.get("state", instance.state)
        instance.allocations = validated_data.get("allocations", instance.allocations)
        instance.team = validated_data.get("group", instance.team)
        instance.team_members = validated_data.get("group_members", instance.team_members)
        return instance
