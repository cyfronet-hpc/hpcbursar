from django.test import TestCase
from grantstorage.localmodels.allocation_usage import AllocationUsage
from datetime import datetime


class TestAllocationUsage(TestCase):
    def create_allocation_usage_model(self, name, summary, usage):
        return AllocationUsage(name=name, summary=summary, usage=usage)

    def test_allocation_usage_model(self):
        name = "plggrant-cpu"
        summary = {"summary": 121423423, "last update": datetime(2020, 5, 17)}
        usage = [{'timestamp': datetime(2020, 5, 17), 'hours': 15},
                 {'timestamp': datetime(2020, 5, 17), 'hours': 10}]

        allocation_usage1 = self.create_allocation_usage_model(name, summary, usage)

        self.assertEquals(allocation_usage1.name, name)
        self.assertEquals(allocation_usage1.summary, summary)
        self.assertEquals(allocation_usage1.usage, usage)
        self.assertEquals(str(allocation_usage1), f"ALLOCATION USAGE: name: {name}, summary: {summary}, usage: {usage}")

    def allocation_usage_serializer(self):
        pass
