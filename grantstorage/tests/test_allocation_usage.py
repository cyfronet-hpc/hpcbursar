from django.test import TestCase
from grantstorage.localmodels.allocation_usage import *
from datetime import datetime


class TestSummary(TestCase):
    @staticmethod
    def create_summary_model(last_update, resources):
        return Summary(last_update, resources)

    def test_summary_model(self):
        last_update = datetime(2020, 5, 17)
        resources = {"hours": 4, "minutes": 5}

        summary_model = self.create_summary_model(last_update, resources)

        self.assertEquals(summary_model.last_update, last_update)
        self.assertEquals(summary_model.resources, resources)
        self.assertEquals(summary_model.__repr__(), f"SUMMARY: last update: {last_update}, summary: {resources}")

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


class TestUsage(TestCase):
    @staticmethod
    def create_usage_model(timestamp, start, end, resources):
        return Usage(timestamp, start, end, resources)

    def test_summary_model(self):
        timestamp = datetime(2020, 5, 17)
        start = datetime(2020, 5, 15)
        end = datetime(2020, 5, 16)
        resources = {"hours": 15, "minutes": 6}
        usage_model = self.create_usage_model(timestamp, start, end, resources)

        self.assertEquals(usage_model.timestamp, timestamp)
        self.assertEqual(usage_model.start, start)
        self.assertEqual(usage_model.end, end)
        self.assertEquals(usage_model.resources, resources)
        self.assertEquals(usage_model.__repr__(),
                          f"USAGE: timestamp: {timestamp}, start: {start}, end: {end}, resources: {resources}")

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


class TestAllocationUsage(TestCase):
    @staticmethod
    def create_allocation_usage_model(name, summary, usage):
        return AllocationUsage(name=name, summary=summary, usage=usage)

    def test_allocation_usage_model(self):
        name = "plggrant-cpu"
        summary = {"resources": {"hours": 4, "minutes": 5}, "last update": datetime(2020, 5, 17)}
        usage = [
            {"timestamp": datetime(2020, 5, 4, 3), "start": datetime(2020, 5, 4, 1), "end": datetime(2020, 5, 4, 2),
             "resources": {"hours": 4, "minutes": 2}},
            {"timestamp": datetime(2020, 5, 5, 7), "start": datetime(2020, 5, 5, 5), "end": datetime(2020, 5, 5, 6),
             "resources": {"hours": 6, "minutes": 1}}]

        allocation_usage_model = self.create_allocation_usage_model(name, summary, usage)

        self.assertEquals(allocation_usage_model.name, name)
        self.assertEquals(allocation_usage_model.summary, summary)
        self.assertEquals(allocation_usage_model.usage, usage)
        self.assertEquals(allocation_usage_model.__repr__(),
                          f"ALLOCATION USAGE: name: {name}, summary: {summary}, usage: {usage}")

    def test_allocation_usage_serializer_contains_expected_fields(self):
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

    def test_allocation_usage_with_data(self):
        data = {
            "name": "plggsoftware",
            "summary": {"last_update": datetime(2020, 5, 7), "resources": {"hours": 10, "minutes": 3}},
            "usage": [
                {"timestamp": datetime(2020, 5, 4, 3), "start": datetime(2020, 5, 4, 1), "end": datetime(2020, 5, 4, 2),
                 "resources": {"hours": 4, "minutes": 2}},
                {"timestamp": datetime(2020, 5, 5, 7), "start": datetime(2020, 5, 5, 5), "end": datetime(2020, 5, 5, 6),
                 "resources": {"hours": 6, "minutes": 1}}]
        }
        serializer = AllocationUsageSerializer(data)
        serializer_data = serializer.data
        self.assertEqual(serializer_data["name"], data["name"])
        self.assertEqual(set(serializer_data.keys()), {"name", "summary", "usage"})
