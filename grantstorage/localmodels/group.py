# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework import serializers


class Group(object):
    def __init__(self, name, status, members, leaders):
        self.name = name
        self.status = status
        self.members = members
        self.leaders = leaders

    def get_all_members(self):
        return list(set(self.members + self.leaders))

    def __str__(self):
        return f'Group: name: {self.name}, status: {self.status}, members: {self.members}, leaders: {self.leaders}'


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField()
    members = serializers.ListField(child=serializers.CharField())
    leaders = serializers.ListField(child=serializers.CharField())

    def create(self, validated_data):
        return Group(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.members = validated_data.get('members', instance.members)
        instance.leaders = validated_data.get('leaders', instance.leaders)
        return instance
