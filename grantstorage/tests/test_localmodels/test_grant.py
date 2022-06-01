from django.test import TestCase
from grantstorage.localmodels.grant import *


class TestAllocations(TestCase):
    @staticmethod
    def create_allocation_model(name, resource, parameters):
        return Allocation(name, resource, parameters)

    def test_allocation_model(self):
        name = "plguser-cpu"
        resource = "CPU"
        parameters = {"timelimit": 72, "hours": 10000000}

        allocation_model = self.create_allocation_model(name, resource, parameters)
        self.assertEqual(allocation_model.name, name)
        self.assertEqual(allocation_model.resource, resource)
        self.assertEqual(allocation_model.parameters, parameters)
        self.assertEqual(allocation_model.__repr__(),
                         f'Allocation: {name}, resource: {resource}, parameters: {parameters}')

    def test_allocation_serializer_contains_expected_fields(self):
        allocation_data = {"name": "plguser-cpu", "resource": "CPU", "parameters": {"timelimit": 72, "hours": 10000000}}
        serializer = AllocationSerializer(allocation_data)
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
        pass


class TestGrant(TestCase):
    @staticmethod
    def create_grant_model(name, group, status, start, end, allocations):
        return Grant(name, group, status, start, end, allocations)

    def test_grant_model(self):
        pass

    def test_grant_serializer_contains_expected_fields(self):
        pass

    def test_grant_serializer_from_model(self):
        pass

    def test_grant_serializer_update(self):
        pass
