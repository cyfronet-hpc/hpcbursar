# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.allocationusage import *
from datetime import datetime


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
