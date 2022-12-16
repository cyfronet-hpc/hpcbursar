# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework import serializers


class Affiliation(object):
    def __init__(self, type, units, status, end):
        self.type = type
        self.units = units
        self.status = status
        self.end = end

    def __str__(self) -> str:
        return f'Affiliation: {self.type} {self.units} {self.status} {self.end}'


class AffiliationSerializer(serializers.Serializer):
    type = serializers.CharField()
    units = serializers.ListField(child=serializers.CharField())
    status = serializers.CharField()
    end = serializers.DateField()

    def create(self, validated_data):
        return Affiliation(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get("type", instance.type)
        instance.units = validated_data.get("units", instance.units)
        instance.status = validated_data.get("status", instance.status)
        instance.end = validated_data.get("end", instance.end)
        return instance


class User(object):
    def __init__(self, login, email, status, first_name, last_name, opi, affiliations):
        self.login = login
        self.email = email
        self.status = status
        self.first_name = first_name
        self.last_name = last_name
        self.opi = opi
        self.affiliations = affiliations

    def __str__(self):
        return f'User: {self.login} {self.email} {self.status} {self.first_name} {self.last_name} {self.opi} {self.affiliations}'


class UserSerializer(serializers.Serializer):
    login = serializers.CharField()
    email = serializers.CharField()
    status = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    opi = serializers.CharField()
    affiliations = AffiliationSerializer()

    def create(self, validated_data):
        affiliations = []
        for a_data in validated_data['affiliations']:
            affiliation = Affiliation(**a_data)
            affiliations.append(affiliation)
        validated_data.update({'affiliations', affiliations})

        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.login = validated_data.get('login', instance.login)
        instance.email = validated_data.get('email', instance.email)
        instance.status = validated_data.get('status', instance.status)
        instance.first_name = validated_data.get('first_name', instance.status)
        instance.last_name = validated_data.get('last_name', instance.status)
        instance.opi = validated_data.get('opi', instance.status)

        affiliations = []
        for a_data in validated_data['affiliations']:
            affiliation = Affiliation(**a_data)
            affiliations.append(affiliation)
        validated_data.update({'affiliations', affiliations})

        instance.affiliations = validated_data.get('affiliations', instance.affiliations)

        return instance
