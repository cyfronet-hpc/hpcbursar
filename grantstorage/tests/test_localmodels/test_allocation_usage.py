# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.allocationusage import *
from datetime import datetime
from collections import OrderedDict


class TestSummary(TestCase):
    @staticmethod
    def create_summary_model(last_update, resources):
        return Summary(last_update, resources)

    def test_summary_model(self):
        last_update = datetime(2020, 5, 17)
        resources = {"hours": 4, "minutes": 5}

        summary_model = self.create_summary_model(last_update, resources)

        self.assertEqual(summary_model.last_update, last_update)
        self.assertEqual(summary_model.resources, resources)
        self.assertEqual(summary_model.__repr__(), f"SUMMARY: last update: {last_update}, summary: {resources}")

    def test_summary_serializer_contains_expected_fields(self):
        summary_data = {"last_update": datetime(2020, 5, 17), "resources": {"hours": 4, "minutes": 5}}
        serializer = SummarySerializer(summary_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'last_update', 'resources'})
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["resources"], {"hours": 4, "minutes": 5})

    def test_summary_serializer_from_model(self):
        last_update = datetime(2020, 5, 17)
        resources = {"hours": 4, "minutes": 5}

        model = self.create_summary_model(last_update, resources)
        serializer = SummarySerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'last_update', 'resources'})
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["resources"], resources)

    def test_summary_serializer_update(self):
        summary_data = {"last_update": datetime(2020, 5, 17), "resources": {"hours": 4, "minutes": 5}}
        serializer = SummarySerializer(data=summary_data)
        self.assertEqual(serializer.is_valid(), True)
        summary = serializer.save()

        new_data = {"last_update": datetime(2022, 6, 1), "resources": {"hours": 10, "minutes": 20}}
        new_model = serializer.update(instance=summary, validated_data=new_data)
        new_serializer = SummarySerializer(new_model)
        new_data = new_serializer.data
        self.assertEqual(set(new_data.keys()), {'last_update', 'resources'})
        self.assertEqual(new_data["last_update"], "2022-06-01T00:00:00Z")
        self.assertNotEqual(new_data["last_update"], "2020-05-17T00:00:00Z")

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
        usage_model = self.create_usage_model(timestamp, start, end, resources)

        self.assertEqual(usage_model.timestamp, timestamp)
        self.assertEqual(usage_model.start, start)
        self.assertEqual(usage_model.end, end)
        self.assertEqual(usage_model.resources, resources)
        self.assertEqual(usage_model.__repr__(),
                         f"USAGE: timestamp: {timestamp}, start: {start}, end: {end}, resources: {resources}")

    def test_usage_serializer_contains_expected_fields(self):
        usage_data = {"timestamp": datetime(2020, 5, 17), "start": datetime(2020, 5, 15), "end": datetime(2020, 5, 16),
                      "resources": {"hours": 15, "minutes": 6}}
        serializer = UsageSerializer(usage_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"timestamp", "start", "end", "resources"})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["start"], "2020-05-15T00:00:00Z")
        self.assertEqual(data["end"], "2020-05-16T00:00:00Z")
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
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["start"], "2020-05-15T00:00:00Z")
        self.assertEqual(data["end"], "2020-05-16T00:00:00Z")
        self.assertEqual(data["resources"], resources)

    def test_usage_serializer_update(self):
        usage_data = {"timestamp": datetime(2020, 5, 17), "start": datetime(2020, 5, 15), "end": datetime(2020, 5, 16),
                      "resources": {"hours": 15, "minutes": 6}}
        serializer = UsageSerializer(data=usage_data)
        self.assertEqual(serializer.is_valid(), True)
        usage = serializer.save()

        new_usage_data = {"timestamp": datetime(2022, 6, 1), "start": datetime(2022, 5, 28),
                          "end": datetime(2022, 5, 30), "resources": {"hours": 20, "minutes": 5}}
        new_model = serializer.update(instance=usage, validated_data=new_usage_data)
        new_serializer = UsageSerializer(new_model)
        new_data = new_serializer.data
        self.assertEqual(set(new_data.keys()), {"timestamp", "start", "end", "resources"})
        self.assertEqual(new_data["timestamp"], "2022-06-01T00:00:00Z")
        self.assertNotEqual(new_data["timestamp"], "2020-05-17T00:00:00Z")

        self.assertEqual(new_data["start"], "2022-05-28T00:00:00Z")
        self.assertNotEqual(new_data["start"], "2022-06-01T00:00:00Z")

        self.assertEqual(new_data["end"], "2022-05-30T00:00:00Z")
        self.assertNotEqual(new_data["end"], "2020-05-16T00:00:00Z")

        self.assertEqual(new_data["resources"], {"hours": 20, "minutes": 5})
        self.assertNotEqual(new_data["resources"], {"hours": 15, "minutes": 6})


class TestAllocationUsage(TestCase):
    @staticmethod
    def create_allocation_usages_model(name, summary, usage):
        return AllocationUsage(name=name, summary=summary, usage=usage)

    def test_allocation_usages_model(self):
        name = "plggrant-cpu"
        summary = {"resources": {"hours": 4, "minutes": 5}, "last update": datetime(2020, 5, 17)}
        usage = [
            {"timestamp": datetime(2020, 5, 4, 3), "start": datetime(2020, 5, 4, 1), "end": datetime(2020, 5, 4, 2),
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": datetime(2020, 5, 5, 7), "start": datetime(2020, 5, 5, 5), "end": datetime(2020, 5, 5, 6),
             "resources": {"hours": 6, "minutes": 1}}]

        allocation_usage_model = self.create_allocation_usages_model(name, summary, usage)

        self.assertEqual(allocation_usage_model.name, name)
        self.assertEqual(allocation_usage_model.summary, summary)
        self.assertEqual(allocation_usage_model.usage, usage)
        self.assertEqual(allocation_usage_model.__repr__(),
                         f"ALLOCATION USAGE: name: {name}, summary: {summary}, usage: {usage}")

    def test_allocation_usages_serializer_contains_expected_fields(self):
        name = "plggrant-cpu"

        summary_last_update = datetime(2020, 5, 17)
        summary_resources = {"hours": 4, "minutes": 5}
        summary_model = Summary(summary_last_update, summary_resources)

        usage_timestamp = datetime(2018, 3, 10)
        usage_start = datetime(2018, 3, 8)
        usage_end = datetime(2018, 3, 9)
        usage_resources = {"hours": 1}
        usage_model = Usage(usage_timestamp, usage_start, usage_end, usage_resources)

        usage_timestamp2 = datetime(2022, 11, 3)
        usage_start_2 = datetime(2022, 11, 1)
        usage_end_2 = datetime(2022, 11, 2)
        usage_resources2 = {"hours": 2, "minutes": 0}
        usage_model2 = Usage(usage_timestamp2, usage_start_2, usage_end_2, usage_resources2)

        allocation_usage_model = AllocationUsage(name, summary_model, [usage_model, usage_model2])
        serializer = AllocationUsageSerializer(allocation_usage_model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'name', "summary", "usage"})

        self.assertEqual(data["name"], name)
        self.assertEqual(data["summary"]["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["summary"]["resources"], summary_resources)

        self.assertEqual(data["usage"][0]["timestamp"], "2018-03-10T00:00:00Z")
        self.assertEqual(data["usage"][0]["start"], "2018-03-08T00:00:00Z")
        self.assertEqual(data["usage"][0]["end"], "2018-03-09T00:00:00Z")
        self.assertEqual(data["usage"][0]["resources"], usage_resources)

        self.assertEqual(data["usage"][1]["timestamp"], "2022-11-03T00:00:00Z")
        self.assertEqual(data["usage"][1]["start"], "2022-11-01T00:00:00Z")
        self.assertEqual(data["usage"][1]["end"], "2022-11-02T00:00:00Z")
        self.assertEqual(data["usage"][1]["resources"], usage_resources2)

    def test_allocation_usages_with_data(self):
        allocation_usages_data = {
            "name": "plggsoftware",
            "summary": {"last_update": datetime(2020, 5, 7), "resources": {"hours": 10, "minutes": 3}},
            "usage": [
                {"timestamp": datetime(2020, 5, 4, 3), "start": datetime(2020, 5, 4, 1), "end": datetime(2020, 5, 4, 2),
                 "resources": {"hours": 4, "minutes": 2}},
                {"timestamp": datetime(2020, 5, 5, 7), "start": datetime(2020, 5, 5, 5), "end": datetime(2020, 5, 5, 6),
                 "resources": {"hours": 6, "minutes": 1}}]
        }
        serializer = AllocationUsageSerializer(allocation_usages_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {"name", "summary", "usage"})
        self.assertEqual(data["name"], "plggsoftware")
        self.assertEqual(data["summary"],
                         OrderedDict({"last_update": "2020-05-07T00:00:00Z", "resources": {"hours": 10, "minutes": 3}}))
        self.assertEqual(data["usage"], [
            {"timestamp": "2020-05-04T03:00:00Z", "start": "2020-05-04T01:00:00Z", "end": "2020-05-04T02:00:00Z",
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": "2020-05-05T07:00:00Z", "start": "2020-05-05T05:00:00Z", "end": "2020-05-05T06:00:00Z",
             "resources": {"hours": 6, "minutes": 1}}])

    def test_allocation_usages_serializer_update(self):
        allocation_usages_data = {
            "name": "plggsoftware",
            "summary": {"last_update": datetime(2020, 5, 7), "resources": {"hours": 10, "minutes": 3}},
            "usage": [
                {"timestamp": datetime(2020, 5, 4, 3), "start": datetime(2020, 5, 4, 1), "end": datetime(2020, 5, 4, 2),
                 "resources": {"hours": 4, "minutes": 2}},
                {"timestamp": datetime(2020, 5, 5, 7), "start": datetime(2020, 5, 5, 5), "end": datetime(2020, 5, 5, 6),
                 "resources": {"hours": 6, "minutes": 1}}]
        }
        serializer = AllocationUsageSerializer(data=allocation_usages_data)
        self.assertEqual(serializer.is_valid(), True)
        allocation_usages = serializer.save()

        new_allocation_usages_data = {
            "name": "plggtraining",
            "summary": {"last_update": datetime(2022, 6, 1), "resources": {"hours": 20, "minutes": 0}},
            "usage": [
                {"timestamp": datetime(2022, 6, 1), "start": datetime(2022, 5, 27, 1), "end": datetime(2022, 5, 30, 2),
                 "resources": {"hours": 10, "minutes": 0}}]
        }
        new_model = serializer.update(instance=allocation_usages, validated_data=new_allocation_usages_data)
        new_serializer = AllocationUsageSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"name", "summary", "usage"})
        self.assertEqual(new_data["name"], "plggtraining")
        self.assertNotEqual(new_data["name"], "plggsoftware")

        self.assertEqual(new_data["summary"],
                         OrderedDict({"last_update": "2022-06-01T00:00:00Z", "resources": {"hours": 20, "minutes": 0}}))
        self.assertNotEqual(new_data["summary"], OrderedDict(
            {"last_update": "2022-05-07T00:00:00Z", "resources": {"hours": 10, "minutes": 3}}))

        self.assertEqual(new_data["usage"], [
            {"timestamp": "2022-06-01T00:00:00Z", "start": "2022-05-27T01:00:00Z", "end": "2022-05-30T02:00:00Z",
             "resources": {"hours": 10, "minutes": 0}}])
        self.assertNotEqual(new_data["usage"], [
            {"timestamp": "2020-05-04T03:00:00Z", "start": "2020-05-04T01:00:00Z", "end": "2020-05-04T02:00:00Z",
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": "2020-05-05T07:00:00Z", "start": "2020-05-05T05:00:00Z", "end": "2020-05-05T06:00:00Z",
             "resources": {"hours": 6, "minutes": 1}}])
