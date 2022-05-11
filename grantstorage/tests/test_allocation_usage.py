from django.test import TestCase
from grantstorage.localmodels.allocation_usage import *
from datetime import datetime


class TestSummary(TestCase):
    @staticmethod
    def create_summary_model(last_update, resources):
        return Summary(last_update, resources)

    def test_summary_model(self):
        last_update1 = datetime(2020, 5, 17)
        resources1 = {"hours": 4, "minutes": 5}

        summary_model = self.create_summary_model(last_update1, resources1)

        self.assertEquals(summary_model.last_update, last_update1)
        self.assertEquals(summary_model.resources, resources1)
        self.assertEquals(summary_model.__repr__(), f"SUMMARY: last update: {last_update1}, summary: {resources1}")

    def test_summary_serializer_contains_expected_fields(self):
        summary_data = {"last_update": datetime(2020, 5, 17), "resources": {"hours": 4, "minutes": 5}}
        serializer = SummarySerializer(summary_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'last_update', 'resources'})
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["resources"], {"hours": 4, "minutes": 5})

    def test_summary_serializer_from_model(self):
        last_update1 = datetime(2020, 5, 17)
        resources1 = {"hours": 4, "minutes": 5}

        model = self.create_summary_model(last_update1, resources1)
        serializer = SummarySerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'last_update', 'resources'})
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["resources"], resources1)


class TestUsage(TestCase):
    @staticmethod
    def create_usage_model(timestamp, resources):
        return Usage(timestamp, resources)

    def test_summary_model(self):
        timestamp1 = datetime(2020, 5, 17)
        resources1 = {"hours": 15, "minutes": 6}
        usage_model = self.create_usage_model(timestamp1, resources1)

        self.assertEquals(usage_model.timestamp, timestamp1)
        self.assertEquals(usage_model.resources, resources1)
        self.assertEquals(usage_model.__repr__(), f"USAGE: timestamp: {timestamp1}, resources: {resources1}")

    def test_usage_serializer_from_model(self):
        timestamp1 = datetime(2020, 5, 17)
        resources1 = {"hours": 4, "minutes": 5}

        model = Usage(timestamp1, resources1)

        serializer = UsageSerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'timestamp', "resources"})
        self.assertEqual(data["timestamp"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["resources"], resources1)


class TestAllocationUsage(TestCase):
    @staticmethod
    def create_allocation_usage_model(name, summary, usage):
        return AllocationUsage(name=name, summary=summary, usage=usage)

    def test_allocation_usage_model(self):
        name1 = "plggrant-cpu"
        summary1 = {"resources": {"hours": 4, "minutes": 5}, "last update": datetime(2020, 5, 17)}
        usage1 = [{'timestamp': datetime(2020, 5, 17), "resources": {"hours": 10}},
                  {'timestamp': datetime(2020, 5, 17), "resources": {"hours": 2, "minutes": 15}}]

        allocation_usage_model = self.create_allocation_usage_model(name1, summary1, usage1)

        self.assertEquals(allocation_usage_model.name, name1)
        self.assertEquals(allocation_usage_model.summary, summary1)
        self.assertEquals(allocation_usage_model.usage, usage1)
        self.assertEquals(allocation_usage_model.__repr__(),
                          f"ALLOCATION USAGE: name: {name1}, summary: {summary1}, usage: {usage1}")

    def test_allocation_usage_serializer_contains_expected_fields(self):
        name = "plggrant-cpu"

        summary_last_update1 = datetime(2020, 5, 17)
        summary_resources1 = {"hours": 4, "minutes": 5}
        summary_model = Summary(summary_last_update1, summary_resources1)

        usage_timestamp1 = datetime(2018, 3, 1)
        usage_resources1 = {"hours": 1}
        usage_model1 = Usage(usage_timestamp1, usage_resources1)

        usage_timestamp2 = datetime(2022, 11, 3)
        usage_resources2 = {"hours": 2, "minutes": 0}
        usage_model2 = Usage(usage_timestamp2, usage_resources2)

        allocation_usage_model = AllocationUsage(name, summary_model, [usage_model1, usage_model2])
        serializer = AllocationUsageSerializer(allocation_usage_model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'name', "summary", "usage"})

        self.assertEqual(data["name"], name)
        self.assertEqual(data["summary"]["last_update"], "2020-05-17T00:00:00Z")
        self.assertEqual(data["summary"]["resources"], summary_resources1)

        self.assertEqual(data["usage"][0]["timestamp"], "2018-03-01T00:00:00Z")
        self.assertEqual(data["usage"][0]["resources"], usage_resources1)

        self.assertEqual(data["usage"][1]["timestamp"], "2022-11-03T00:00:00Z")
        self.assertEqual(data["usage"][1]["resources"], usage_resources2)
