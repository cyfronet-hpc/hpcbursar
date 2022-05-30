from django.test import TestCase
from grantstorage.localmodels.user import *


class TestUser(TestCase):
    def create_user_model(self, login, status):
        return User(login, status)

    def test_user_model(self):
        login = "plgadmin"
        status = "ACTIVE"

        user_model = self.create_user_model(login, status)
        self.assertEqual(user_model.login, login)
        self.assertEqual(user_model.status, status)
        self.assertEqual(user_model.__str__(), f'User: {login} {status}')

    def test_user_serializer_contains_expected_fields(self):
        user_data = {"login": "plgadmin", "status": "ACTIVE"}
        serializer = UserSerializer(user_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"login", "status"})
        self.assertEqual(data["login"], "plgadmin")
        self.assertEqual(data["status"], "ACTIVE")

    def test_user_serializer_from_model(self):
        pass
