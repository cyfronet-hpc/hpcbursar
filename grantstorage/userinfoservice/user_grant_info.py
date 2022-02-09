from rest_framework import serializers


class UserGrantInfoResponse(object):
    def __init__(self, grant, group):
        self.name = grant.name
        self.start = grant.start
        self.end = grant.end
        self.state = group.status
        self.allocations = grant.allocations
        self.group = grant.group
        self.group_members = group.members

    def __str__(self):
        return f"Grant name: {self.name}, start: {self.start}, end: {self.end}, state: {self.state}, " \
               f"allocations: {self.allocations}, group: {self.group}, group members: {self.group_members}"


class UserGrantInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    state = serializers.CharField()
    allocations = serializers.ListField(child=serializers.CharField())
    group = serializers.CharField()
    group_members = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return UserGrantInfoResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.start = validated_data.get("start", instance.start)
        instance.end = validated_data.get("end", instance.end)
        instance.state = validated_data.get("state", instance.state)
        instance.allocations = validated_data.get("allocations", instance.allocations)
        instance.team = validated_data.get("group", instance.team)
        instance.team_members = validated_data.get("group_members", instance.team_members)
        return instance
