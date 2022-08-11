# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.group import *


class TestGroup(TestCase):
    @staticmethod
    def create_group_model(name, status, members, leaders):
        return Group(name, status, members, leaders)

    def test_group_model(self):
        name = "test_group"
        status = "ACCEPTED"
        members = ["plguser1", "plguser2", "plguser3"]
        leaders = ["plgadmin", "plguser1"]

        group_model = self.create_group_model(name, status, members, leaders)
        self.assertEqual(group_model.name, name)
        self.assertEqual(group_model.status, status)
        self.assertEqual(group_model.members, members)
        self.assertEqual(group_model.leaders, leaders)
        self.assertEqual(group_model.__str__(),
                         f'Group: name: {name}, status: {status}, members: {members}, leaders: {leaders}')

    def test_group_serializer_contains_expected_values(self):
        group_data = {"name": "test_group", "status": "ACCEPTED", "members": ["plguser1", "plguser2", "plguser3"],
                      "leaders": ["plgadmin", "plguser1"]}
        serializer = GroupSerializer(group_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"name", "status", "members", "leaders"})
        self.assertEqual(data["name"], "test_group")
        self.assertEqual(data["status"], "ACCEPTED")
        self.assertEqual(data["members"], ["plguser1", "plguser2", "plguser3"])
        self.assertEqual(data["leaders"], ["plgadmin", "plguser1"])

    def test_group_serializer_from_model(self):
        name = "test_group"
        status = "ACCEPTED"
        members = ["plguser1", "plguser2", "plguser3"]
        leaders = ["plgadmin", "plguser1"]

        model = self.create_group_model(name, status, members, leaders)
        serializer = GroupSerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"name", "status", "members", "leaders"})
        self.assertEqual(data["name"], "test_group")
        self.assertEqual(data["status"], "ACCEPTED")
        self.assertEqual(data["members"], ["plguser1", "plguser2", "plguser3"])
        self.assertEqual(data["leaders"], ["plgadmin", "plguser1"])

    def test_group_serializer_update(self):
        group_data = {"name": "test_group", "status": "ACCEPTED", "members": ["plguser1", "plguser2", "plguser3"],
                      "leaders": ["plgadmin", "plguser1"]}
        serializer = GroupSerializer(data=group_data)
        self.assertEqual(serializer.is_valid(), True)
        group = serializer.save()

        new_group_data = {"name": "new_test_group", "status": "INACTIVE",
                          "members": ["plgnewuser1", "plgnewuser2", "plgnewuser3"],
                          "leaders": ["plgnewadmin"]}
        new_model = serializer.update(instance=group, validated_data=new_group_data)
        new_serializer = GroupSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "status", "members", "leaders"})
        self.assertEqual(new_data["name"], "new_test_group")
        self.assertNotEqual(new_data["name"], "test_group")

        self.assertEqual(new_data["status"], "INACTIVE")
        self.assertNotEqual(new_data["status"], "ACCEPTED")

        self.assertEqual(new_data["members"], ["plgnewuser1", "plgnewuser2", "plgnewuser3"])
        self.assertNotEqual(new_data["members"], ["plguser1", "plguser2", "plguser3"])

        self.assertEqual(new_data["leaders"], ["plgnewadmin"])
        self.assertNotEqual(new_data["leaders"], ["plgadmin", "plguser1"])
