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
