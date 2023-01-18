# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.allocationusage import *
from datetime import datetime
from collections import OrderedDict


class TestSummary(TestCase):
    @staticmethod
    def create_summary_model(timestamp, resources):
        return Summary(timestamp, resources)

    def test_summary_model(self):
        timestamp = datetime(2020, 5, 17)
        resources = {"hours": 4, "minutes": 5}
        model = self.create_summary_model(timestamp, resources)

        self.assertEqual(model.timestamp, timestamp)
        self.assertEqual(model.resources, resources)
        self.assertEqual(model.__repr__(), f"Summary: timestamp: {timestamp}, summary: {resources}")

    def test_summary_serializer_contains_expected_fields(self):
        data = {"timestamp": datetime(2020, 5, 17),
                "resources": {"hours": 4, "minutes": 5}}
        serializer = SummarySerializer(data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {'timestamp', 'resources'})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00")
        self.assertEqual(data["resources"], {"hours": 4, "minutes": 5})

    def test_summary_serializer_from_model(self):
        timestamp = datetime(2020, 5, 17)
        resources = {"hours": 4, "minutes": 5}
        model = self.create_summary_model(timestamp, resources)
        serializer = SummarySerializer(model)
        data = serializer.data

        self.assertEqual(set(data.keys()), {'timestamp', 'resources'})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00")
        self.assertEqual(data["resources"], resources)

    def test_summary_serializer_update(self):
        data = {"timestamp": datetime(2020, 5, 17),
                "resources": {"hours": 4, "minutes": 5}}
        serializer = SummarySerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        summary = serializer.save()

        new_data = {"timestamp": datetime(2022, 6, 1),
                    "resources": {"hours": 10, "minutes": 20}}
        new_model = serializer.update(instance=summary, validated_data=new_data)
        new_serializer = SummarySerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {'timestamp', 'resources'})
        self.assertEqual(new_data["timestamp"], "2022-06-01T00:00:00")
        self.assertNotEqual(new_data["timestamp"], "2020-05-17T00:00:00")

        self.assertEqual(new_data["resources"], {"hours": 10, "minutes": 20})
        self.assertNotEqual(new_data["resources"], {"hours": 4, "minutes": 5})


class TestUsage(TestCase):
    @staticmethod
    def create_usage_model(timestamp, start, end, resources):
        return Usage(timestamp, start, end, resources)

    def test_usage_model(self):
        timestamp = datetime(2020, 5, 17)
        start = datetime(2020, 5, 15)
        end = datetime(2020, 5, 16)
        resources = {"hours": 15, "minutes": 6}
        model = self.create_usage_model(timestamp, start, end, resources)

        self.assertEqual(model.timestamp, timestamp)
        self.assertEqual(model.start, start)
        self.assertEqual(model.end, end)
        self.assertEqual(model.resources, resources)
        self.assertEqual(model.__repr__(),
                         f"Usage: timestamp: {timestamp}, start: {start}, end: {end}, resources: {resources}")

    def test_usage_serializer_contains_expected_fields(self):
        data = {"timestamp": datetime(2020, 5, 17),
                "start": datetime(2020, 5, 15),
                "end": datetime(2020, 5, 16),
                "resources": {"hours": 15, "minutes": 6}}
        serializer = UsageSerializer(data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"timestamp", "start", "end", "resources"})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00")
        self.assertEqual(data["start"], "2020-05-15T00:00:00")
        self.assertEqual(data["end"], "2020-05-16T00:00:00")
        self.assertEqual(data["resources"], {"hours": 15, "minutes": 6})

    def test_usage_serializer_from_model(self):
        timestamp = datetime(2020, 5, 17)
        start = datetime(2020, 5, 15)
        end = datetime(2020, 5, 16)
        resources = {"hours": 4, "minutes": 5}
        model = Usage(timestamp, start, end, resources)
        serializer = UsageSerializer(model)
        data = serializer.data

        self.assertEqual(set(data.keys()), {'timestamp', "start", "end", "resources"})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00")
        self.assertEqual(data["start"], "2020-05-15T00:00:00")
        self.assertEqual(data["end"], "2020-05-16T00:00:00")
        self.assertEqual(data["resources"], resources)

    def test_usage_serializer_update(self):
        data = {"timestamp": datetime(2020, 5, 17),
                "start": datetime(2020, 5, 15),
                "end": datetime(2020, 5, 16),
                "resources": {"hours": 15, "minutes": 6}}
        serializer = UsageSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        usage = serializer.save()

        new_data = {"timestamp": datetime(2022, 6, 1),
                    "start": datetime(2022, 5, 28),
                    "end": datetime(2022, 5, 30),
                    "resources": {"hours": 20, "minutes": 5}}
        new_model = serializer.update(instance=usage, validated_data=new_data)
        new_serializer = UsageSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"timestamp", "start", "end", "resources"})
        self.assertEqual(new_data["timestamp"], "2022-06-01T00:00:00")
        self.assertNotEqual(new_data["timestamp"], "2020-05-17T00:00:00")

        self.assertEqual(new_data["start"], "2022-05-28T00:00:00")
        self.assertNotEqual(new_data["start"], "2022-06-01T00:00:00")

        self.assertEqual(new_data["end"], "2022-05-30T00:00:00")
        self.assertNotEqual(new_data["end"], "2020-05-16T00:00:00")

        self.assertEqual(new_data["resources"], {"hours": 20, "minutes": 5})
        self.assertNotEqual(new_data["resources"], {"hours": 15, "minutes": 6})


class TestAllocationUsage(TestCase):
    @staticmethod
    def create_allocation_usages_model(name, summary, usages):
        return AllocationUsage(name, summary, usages)

    def test_allocation_usages_model(self):
        name = "plggrant-cpu"
        summary = {"timestamp": datetime(2020, 5, 17),
                   "resources": {"hours": 4, "minutes": 5}}
        usages = [{"timestamp": datetime(2020, 5, 4, 3),
                   "start": datetime(2020, 5, 4, 1),
                   "end": datetime(2020, 5, 4, 2),
                   "resources": {"hours": 4, "minutes": 2}},
                  {"timestamp": datetime(2020, 5, 5, 7),
                   "start": datetime(2020, 5, 5, 5),
                   "end": datetime(2020, 5, 5, 6),
                   "resources": {"hours": 6, "minutes": 1}}]
        model = self.create_allocation_usages_model(name, summary, usages)

        self.assertEqual(model.name, name)
        self.assertEqual(model.summary, summary)
        self.assertEqual(model.usages, usages)
        self.assertEqual(model.__repr__(), f"AllocationUsage: name: {name}, summary: {summary}, usage: {usages}")

    def test_allocation_usages_serializer_contains_expected_fields(self):
        name = "plggrant-cpu"

        summary_timestamp = datetime(2020, 5, 17)
        summary_resources = {"hours": 4, "minutes": 5}
        summary_model = Summary(summary_timestamp, summary_resources)

        usages_timestamp = datetime(2018, 3, 10)
        usages_start = datetime(2018, 3, 8)
        usages_end = datetime(2018, 3, 9)
        usages_resources = {"hours": 1}
        usages_model = Usage(usages_timestamp, usages_start, usages_end, usages_resources)

        usages_timestamp2 = datetime(2022, 11, 3)
        usages_start_2 = datetime(2022, 11, 1)
        usages_end_2 = datetime(2022, 11, 2)
        usages_resources_2 = {"hours": 2, "minutes": 0}
        usages_model_2 = Usage(usages_timestamp2, usages_start_2, usages_end_2, usages_resources_2)

        model = AllocationUsage(name, summary_model, [usages_model, usages_model_2])
        serializer = AllocationUsageSerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'name', "summary", "usages"})

        self.assertEqual(data["name"], name)
        self.assertEqual(data["summary"]["timestamp"], "2020-05-17T00:00:00")
        self.assertEqual(data["summary"]["resources"], summary_resources)

        self.assertEqual(data["usages"][0]["timestamp"], "2018-03-10T00:00:00")
        self.assertEqual(data["usages"][0]["start"], "2018-03-08T00:00:00")
        self.assertEqual(data["usages"][0]["end"], "2018-03-09T00:00:00")
        self.assertEqual(data["usages"][0]["resources"], usages_resources)

        self.assertEqual(data["usages"][1]["timestamp"], "2022-11-03T00:00:00")
        self.assertEqual(data["usages"][1]["start"], "2022-11-01T00:00:00")
        self.assertEqual(data["usages"][1]["end"], "2022-11-02T00:00:00")
        self.assertEqual(data["usages"][1]["resources"], usages_resources_2)

    def test_allocation_usages_with_data(self):
        data = {"name": "plggsoftware",
                "summary": {"timestamp": datetime(2020, 5, 7),
                            "resources": {"hours": 10, "minutes": 3}},
                "usages": [{"timestamp": datetime(2020, 5, 4, 3),
                            "start": datetime(2020, 5, 4, 1),
                            "end": datetime(2020, 5, 4, 2),
                            "resources": {"hours": 4, "minutes": 2}},
                           {"timestamp": datetime(2020, 5, 5, 7),
                            "start": datetime(2020, 5, 5, 5),
                            "end": datetime(2020, 5, 5, 6),
                            "resources": {"hours": 6, "minutes": 1}}]}
        serializer = AllocationUsageSerializer(data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"name", "summary", "usages"})
        self.assertEqual(data["name"], "plggsoftware")
        self.assertEqual(data["summary"],
                         OrderedDict({"timestamp": "2020-05-07T00:00:00", "resources": {"hours": 10, "minutes": 3}}))
        self.assertEqual(data["usages"], [
            {"timestamp": "2020-05-04T03:00:00", "start": "2020-05-04T01:00:00", "end": "2020-05-04T02:00:00",
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": "2020-05-05T07:00:00", "start": "2020-05-05T05:00:00", "end": "2020-05-05T06:00:00",
             "resources": {"hours": 6, "minutes": 1}}])

    def test_allocation_usages_serializer_update(self):
        data = {"name": "plggsoftware",
                "summary": {"timestamp": datetime(2020, 5, 7),
                            "resources": {"hours": 10, "minutes": 3}},
                "usages": [{"timestamp": datetime(2020, 5, 4, 3),
                            "start": datetime(2020, 5, 4, 1),
                            "end": datetime(2020, 5, 4, 2),
                            "resources": {"hours": 4, "minutes": 2}},
                           {"timestamp": datetime(2020, 5, 5, 7),
                            "start": datetime(2020, 5, 5, 5),
                            "end": datetime(2020, 5, 5, 6),
                            "resources": {"hours": 6, "minutes": 1}}]}
        serializer = AllocationUsageSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        allocation_usages = serializer.save()

        new_data = {
            "name": "plggtraining",
            "summary": {"timestamp": datetime(2022, 6, 1),
                        "resources": {"hours": 20, "minutes": 0}},
            "usages": [{"timestamp": datetime(2022, 6, 1),
                        "start": datetime(2022, 5, 27, 1),
                        "end": datetime(2022, 5, 30, 2),
                        "resources": {"hours": 10, "minutes": 0}}]}
        new_model = serializer.update(instance=allocation_usages, validated_data=new_data)
        new_serializer = AllocationUsageSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "summary", "usages"})
        self.assertEqual(new_data["name"], "plggtraining")
        self.assertNotEqual(new_data["name"], "plggsoftware")

        self.assertEqual(new_data["summary"],
                         OrderedDict({"timestamp": "2022-06-01T00:00:00", "resources": {"hours": 20, "minutes": 0}}))
        self.assertNotEqual(new_data["summary"], OrderedDict(
            {"timestamp": "2022-05-07T00:00:00", "resources": {"hours": 10, "minutes": 3}}))

        self.assertEqual(new_data["usages"], [
            {"timestamp": "2022-06-01T00:00:00", "start": "2022-05-27T01:00:00", "end": "2022-05-30T02:00:00",
             "resources": {"hours": 10, "minutes": 0}}])
        self.assertNotEqual(new_data["usages"], [
            {"timestamp": "2020-05-04T03:00:00", "start": "2020-05-04T01:00:00", "end": "2020-05-04T02:00:00",
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": "2020-05-05T07:00:00", "start": "2020-05-05T05:00:00", "end": "2020-05-05T06:00:00",
             "resources": {"hours": 6, "minutes": 1}}])
