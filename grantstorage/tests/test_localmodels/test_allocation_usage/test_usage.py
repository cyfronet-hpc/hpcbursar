# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.allocationusage import *
from datetime import datetime


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
