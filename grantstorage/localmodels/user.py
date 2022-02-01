from rest_framework import serializers


class User(object):
    def __init__(self, login, status):
        self.login = login
        self.status = status

    def __str__(self):
        return f'User: {self.login} {self.status}'


class UserSerializer(serializers.Serializer):
    login = serializers.CharField()
    status = serializers.CharField()

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.login = validated_data.get('login', instance.login)
        instance.status = validated_data.get('status', instance.status)
        return instance