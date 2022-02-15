from rest_framework import serializers


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


class UserGrantInfoResponse(object):
    def __init__(self, grant, group):
        self.name = grant.name
        self.start = grant.start
        self.end = grant.end
        self.state = grant.status
        self.allocations = [UserGrantInfoAllocation(allocation) for allocation in grant.allocations]
        self.group = grant.group
        self.group_members = group.members + group.leaders

    def __str__(self):
        return f"Grant name: {self.name}, start: {self.start}, end: {self.end}, state: {self.state}, " \
               f"allocations: {self.allocations}, group: {self.group}, group members: {self.group_members}"


class UserGrantInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    state = serializers.CharField()
    allocations = UserGrantInfoAllocationSerializer(many=True)
    group = serializers.CharField()
    group_members = serializers.ListField(child=serializers.CharField())

    # def create(self, validated_data):
    #     return UserGrantInfoResponse(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.start = validated_data.get("start", instance.start)
    #     instance.end = validated_data.get("end", instance.end)
    #     instance.state = validated_data.get("state", instance.state)
    #     instance.allocations = validated_data.get("allocations", instance.allocations)
    #     instance.team = validated_data.get("group", instance.team)
    #     instance.team_members = validated_data.get("group_members", instance.team_members)
    #     return instance
