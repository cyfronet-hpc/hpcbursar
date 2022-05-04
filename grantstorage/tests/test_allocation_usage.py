from django.test import TestCase
from grantstorage.localmodels.allocation_usage import *
from datetime import datetime


class TestSummary(TestCase):
    @staticmethod
    def create_summary_model(summary, last_update):
        return Summary(summary, last_update)

    def test_summary_model(self):
        summary1 = "121423423"
        last_update1 = datetime(2020, 5, 17)

        summary_model = self.create_summary_model(summary1, last_update1)

        self.assertEquals(summary_model.summary, summary1)
        self.assertEquals(summary_model.last_update, last_update1)
        self.assertEquals(summary_model.__repr__(), f"SUMMARY: summary: {summary1}, last update: {last_update1}")

    def test_summary_serializer_contains_expected_fields(self):
        summary_data = {"summary": "121423423", "last_update": datetime(2020, 5, 17)}
        serializer = SummarySerializer(summary_data)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'summary', 'last_update'})
        self.assertEqual(data["summary"], "121423423")
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")

    def test_summary_serializer_from_model(self):
        summary1 = "121423423"
        last_update1 = datetime(2020, 5, 17)

        model = self.create_summary_model(summary1, last_update1)
        serializer = SummarySerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'summary', 'last_update'})
        self.assertEqual(data["summary"], summary1)
        self.assertEqual(data["last_update"], "2020-05-17T00:00:00Z")


class TestUsage(TestCase):
    @staticmethod
    def create_usage_model(usage):
        return Usage(usage)

    def test_summary_model(self):
        usage = {"timestamp": datetime(2020, 1, 1), "hours": 15}
        usage_model = self.create_usage_model(usage)

        self.assertEquals(usage_model.usage, usage)
        self.assertEquals(usage_model.__repr__(), f"USAGE: usage: {usage}")

    def test_usage_serializer_contains_expected_fields(self):
        usage_data = [{"timestamp": datetime(2020, 1, 1), "hours": 15},
                      {"timestamp": datetime(2017, 5, 7), "hours": 10}]

        model = Usage(usage_data)
        serializer = UsageSerializer(model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'usage'})
        self.assertEqual(data["usage"], usage_data)
        self.assertEqual(data["usage"][0], {"timestamp": datetime(2020, 1, 1), "hours": 15})
        self.assertEqual(data["usage"][1], {"timestamp": datetime(2017, 5, 7), "hours": 10})

        self.assertEqual(data["usage"][0]["timestamp"], datetime(2020, 1, 1))
        self.assertEqual(data["usage"][0]["hours"], 15)

        self.assertEqual(data["usage"][1]["timestamp"], datetime(2017, 5, 7))
        self.assertEqual(data["usage"][1]["hours"], 10)


class TestAllocationUsage(TestCase):
    @staticmethod
    def create_allocation_usage_model(name, summary, usage):
        return AllocationUsage(name=name, summary=summary, usage=usage)

    def test_allocation_usage_model(self):
        name1 = "plggrant-cpu"
        summary1 = {"summary": 121423423, "last update": datetime(2020, 5, 17)}
        usage1 = [{'timestamp': datetime(2020, 5, 17), 'hours': 15},
                  {'timestamp': datetime(2020, 5, 17), 'hours': 10}]

        allocation_usage_model = self.create_allocation_usage_model(name1, summary1, usage1)

        self.assertEquals(allocation_usage_model.name, name1)
        self.assertEquals(allocation_usage_model.summary, summary1)
        self.assertEquals(allocation_usage_model.usage, usage1)
        self.assertEquals(allocation_usage_model.__repr__(),
                          f"ALLOCATION USAGE: name: {name1}, summary: {summary1}, usage: {usage1}")

    def test_allocation_usage_serializer_contains_expected_fields(self):
        name = "plggrant-cpu"

        summary1 = "121423423"
        last_update1 = datetime(2020, 5, 17)
        summary_model = Summary(summary1, last_update1)

        usage_data = [{"timestamp": datetime(2020, 1, 8), "hours": 20},
                      {"timestamp": datetime(2019, 5, 7), "hours": 10}]
        usage_model = Usage(usage_data)

        allocation_usage_model = AllocationUsage(name, summary_model, usage_model)
        serializer = AllocationUsageSerializer(allocation_usage_model)
        data = serializer.data
        self.assertEqual(set(data.keys()), {'name', "summary", "usage"})

        self.assertEqual(data["name"], name)

        self.assertEqual(data["summary"]["summary"], '121423423')
        self.assertEqual(data["summary"]["last_update"], '2020-05-17T00:00:00Z')

        self.assertEqual(data["usage"]["usage"], usage_data)
        self.assertEqual(data["usage"]["usage"][0], usage_data[0])
        self.assertEqual(data["usage"]["usage"][1], usage_data[1])
