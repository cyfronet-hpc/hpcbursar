# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.grant import *


class TestAllocation(TestCase):
    @staticmethod
    def create_allocation_model(name, resource, parameters):
        return Allocation(name, resource, parameters)

    def test_allocation_model(self):
        name = "plguser-cpu"
        resource = "CPU"
        parameters = {"timelimit": 72, "hours": 10000000}
        model = self.create_allocation_model(name, resource, parameters)

        self.assertEqual(model.name, name)
        self.assertEqual(model.resource, resource)
        self.assertEqual(model.parameters, parameters)
        self.assertEqual(model.__repr__(), f'Allocation: {name}, resource: {resource}, parameters: {parameters}')

    def test_allocation_serializer_contains_expected_fields(self):
        data = {"name": "plguser-cpu",
                "resource": "CPU",
                "parameters": {"timelimit": 72, "hours": 10000000}}
        serializer = AllocationSerializer(data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"name", "resource", "parameters"})
        self.assertEqual(data["name"], "plguser-cpu")
        self.assertEqual(data["resource"], "CPU")
        self.assertEqual(data["parameters"], {"timelimit": 72, "hours": 10000000})

    def test_allocation_serializer_from_model(self):
        name = "plguser-cpu"
        resource = "CPU"
        parameters = {"timelimit": 72, "hours": 10000000}
        model = self.create_allocation_model(name, resource, parameters)
        serializer = AllocationSerializer(model)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"name", "resource", "parameters"})
        self.assertEqual(data["name"], "plguser-cpu")
        self.assertEqual(data["resource"], "CPU")
        self.assertEqual(data["parameters"], {"timelimit": 72, "hours": 10000000})

    def test_allocation_serializer_update(self):
        data = {"name": "plguser-cpu",
                "resource": "CPU",
                "parameters": {"timelimit": 72, "hours": 10000000}}
        serializer = AllocationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        allocation = serializer.save()

        new_data = {"name": "plguser-gpu",
                    "resource": "GPU",
                    "parameters": {"timelimit": 10, "hours": 2000}}
        new_model = serializer.update(instance=allocation, validated_data=new_data)
        new_serializer = AllocationSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "resource", "parameters"})
        self.assertEqual(new_data["name"], "plguser-gpu")
        self.assertNotEqual(new_data["name"], "tplguser-cpu")

        self.assertEqual(new_data["resource"], "GPU")
        self.assertNotEqual(new_data["resource"], "CPU")

        self.assertEqual(new_data["parameters"], {"timelimit": 10, "hours": 2000})
        self.assertNotEqual(new_data["parameters"], {"timelimit": 72, "hours": 10000000})
