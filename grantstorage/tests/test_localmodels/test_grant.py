# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.grant import *
import datetime


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
        allocation_data = {"name": "plguser-cpu",
                           "resource": "CPU",
                           "parameters": {"timelimit": 72, "hours": 10000000}}
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
        allocation_data = {"name": "plguser-cpu",
                           "resource": "CPU",
                           "parameters": {"timelimit": 72, "hours": 10000000}}
        serializer = AllocationSerializer(data=allocation_data)
        self.assertEqual(serializer.is_valid(), True)
        allocation = serializer.save()

        new_allocation_data = {"name": "plguser-gpu",
                               "resource": "GPU",
                               "parameters": {"timelimit": 10, "hours": 2000}}
        new_model = serializer.update(instance=allocation, validated_data=new_allocation_data)
        new_serializer = AllocationSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "resource", "parameters"})
        self.assertEqual(new_data["name"], "plguser-gpu")
        self.assertNotEqual(new_data["name"], "tplguser-cpu")

        self.assertEqual(new_data["resource"], "GPU")
        self.assertNotEqual(new_data["resource"], "CPU")

        self.assertEqual(new_data["parameters"], {"timelimit": 10, "hours": 2000})
        self.assertNotEqual(new_data["parameters"], {"timelimit": 72, "hours": 10000000})


class TestGrant(TestCase):
    @staticmethod
    def create_grant_model(name, group, status, start, end, allocations):
        return Grant(name, group, status, start, end, allocations)

    def test_grant_model(self):
        name = "plgplgrid"
        group = "plggplgrid"
        status = "grant_active"
        start = datetime.date(2009, 10, 11)
        end = datetime.date(2009, 10, 14)
        allocations = Allocation("plguser-cpu", "CPU", {"timelimit": 72, "hours": 10000000})
        grant_model = self.create_grant_model(name, group, status, start, end, allocations)

        self.assertEqual(grant_model.name, name)
        self.assertEqual(grant_model.group, group)
        self.assertEqual(grant_model.status, status)
        self.assertEqual(grant_model.start, start)
        self.assertEqual(grant_model.end, end)
        self.assertEqual(grant_model.allocations, allocations)

    def test_grant_serializer_contains_expected_fields(self):
        grant_data = {"name": "plgplgrid",
                      "group": "plggplgrid",
                      "status": "grant_active",
                      "start": datetime.date(2009, 10, 11),
                      "end": datetime.date(2009, 10, 14),
                      "allocations": [{"name": "plghb9-cpu",
                                       "resource": "CPU",
                                       "parameters": {"timelimit": 72, "hours": 30000000}},
                                      {"name": "plghb9-storage",
                                       "resource": "Storage",
                                       "parameters": {"capacity": 20000}}]}
        serializer = GrantSerializer(grant_data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"name", "group", "status", "start", "end", "allocations"})
        self.assertEqual(data["name"], "plgplgrid")
        self.assertEqual(data["group"], "plggplgrid")
        self.assertEqual(data["status"], "grant_active")
        self.assertEqual(data["start"], "2009-10-11")
        self.assertEqual(data["end"], "2009-10-14")
        self.assertEqual(data["allocations"], [
            {"name": "plghb9-cpu", "resource": "CPU", "parameters": {"timelimit": 72, "hours": 30000000}},
            {"name": "plghb9-storage", "resource": "Storage", "parameters": {"capacity": 20000}}])

    def test_grant_serializer_from_model(self):
        name = "plgplgrid"
        group = "plggplgrid"
        status = "grant_active"
        start = datetime.date(2009, 10, 11)
        end = datetime.date(2009, 10, 14)
        allocation_1 = Allocation("plghb9-cpu", "CPU", {"timelimit": 72, "hours": 30000000})
        allocation_2 = Allocation("plghb9-storage", "Storage", {"capacity": 20000})
        grant_model = self.create_grant_model(name, group, status, start, end, [allocation_1, allocation_2])
        serializer = GrantSerializer(grant_model)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"name", "group", "status", "start", "end", "allocations"})
        self.assertEqual(data["name"], "plgplgrid")
        self.assertEqual(data["group"], "plggplgrid")
        self.assertEqual(data["status"], "grant_active")
        self.assertEqual(data["start"], "2009-10-11")
        self.assertEqual(data["end"], "2009-10-14")
        self.assertEqual(data["allocations"], [
            {"name": "plghb9-cpu", "resource": "CPU", "parameters": {"timelimit": 72, "hours": 30000000}},
            {"name": "plghb9-storage", "resource": "Storage", "parameters": {"capacity": 20000}}])

    def test_grant_serializer_update(self):
        grant_data = {"name": "plgplgrid",
                      "group": "plggplgrid",
                      "status": "grant_active",
                      "start": datetime.date(2009, 10, 11),
                      "end": datetime.date(2009, 10, 14),
                      "allocations": [{"name": "plghb9-cpu",
                                       "resource": "CPU",
                                       "parameters": {"timelimit": 72, "hours": 30000000}},
                                      {"name": "plghb9-storage",
                                       "resource": "Storage",
                                       "parameters": {"capacity": 20000}}]}
        serializer = GrantSerializer(data=grant_data)
        self.assertEqual(serializer.is_valid(), True)
        grant = serializer.save()

        new_grant_data = {"name": "test_plgplgrid",
                          "group": "test_plggplgrid",
                          "status": "grant_inactive",
                          "start": datetime.date(2011, 10, 11),
                          "end": datetime.date(2011, 10, 14),
                          "allocations": [{"name": "plg-gpu",
                                           "resource": "GPU",
                                           "parameters": {"timelimit": 10, "hours": 2000}}]}
        new_model = serializer.update(instance=grant, validated_data=new_grant_data)
        new_serializer = GrantSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "group", "status", "start", "end", "allocations"})
        self.assertEqual(new_data["name"], "test_plgplgrid")
        self.assertNotEqual(new_data["name"], "plgplgrid")

        self.assertEqual(new_data["group"], "test_plggplgrid")
        self.assertNotEqual(new_data["group"], "plggplgrid")

        self.assertEqual(new_data["status"], "grant_inactive")
        self.assertNotEqual(new_data["status"], "grant_active")

        self.assertEqual(new_data["start"], "2011-10-11")
        self.assertNotEqual(new_data["start"], "2009-10-11")

        self.assertEqual(new_data["end"], "2011-10-14")
        self.assertNotEqual(new_data["end"], "2009-10-14")

        self.assertEqual(new_data["allocations"], [
            {"name": "plg-gpu", "resource": "GPU", "parameters": {"timelimit": 10, "hours": 2000}}])
        self.assertNotEqual(new_data["allocations"], [
            {"name": "plghb9-cpu", "resource": "CPU", "parameters": {"timelimit": 72, "hours": 30000000}},
            {"name": "plghb9-storage", "resource": "Storage", "parameters": {"capacity": 20000}}])
