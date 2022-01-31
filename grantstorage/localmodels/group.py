from rest_framework import serializers


class Group(object):
    def __init__(self, name, status, members, leaders):
        self.name = name
        self.status = status
        self.members = members
        self.leaders = leaders

    def __str__(self):
        return f'Group: name: {self.name}, status: {self.status}, members: {self.members}'


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField())
    leaders = serializers.ListField(child=serializers.CharField())
