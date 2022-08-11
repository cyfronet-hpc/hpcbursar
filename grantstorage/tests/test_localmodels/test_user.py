# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.user import *


class TestUser(TestCase):
    @staticmethod
    def create_user_model(login, status):
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
        login = "plgadmin"
        status = "ACTIVE"

        model = self.create_user_model(login, status)
        serializer = UserSerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"login", "status"})
        self.assertEqual(data["login"], "plgadmin")
        self.assertEqual(data["status"], "ACTIVE")

    def test_user_serializer_update(self):
        user_data = {"login": "plgadmin", "status": "ACTIVE"}
        serializer = UserSerializer(data=user_data)
        self.assertEqual(serializer.is_valid(), True)
        user = serializer.save()

        new_data = {"login": "plgnewadmin", "status": "INACTIVE"}
        new_model = serializer.update(instance=user, validated_data=new_data)
        new_serializer = UserSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"login", "status"})
        self.assertEqual(new_data["login"], "plgnewadmin")
        self.assertNotEqual(new_data["login"], "plgadmin")

        self.assertEqual(new_data["status"], "INACTIVE")
        self.assertNotEqual(new_data["login"], "ACTIVE")
