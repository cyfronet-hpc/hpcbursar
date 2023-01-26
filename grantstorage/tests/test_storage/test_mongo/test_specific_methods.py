# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from .helper_functions import *


# TODO: NOT WORKING
class TestMongoStorageSpecificMethods(TestCase):
    def test_update_usage_in_allocation_usages(self):
        ms = MongoStorage()
        allocation_usage = AllocationUsage("update_test_name",
                                           {"last_update": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                            "resources": {"hours": 20, "minutes": 3}},
                                           [{"timestamp": datetime(2011, 5, 10, tzinfo=timezone.utc),
                                             "start": datetime(2011, 5, 8, tzinfo=timezone.utc),
                                             "end": datetime(2011, 5, 10, tzinfo=timezone.utc),
                                             "resources": {"hours": 15, "minutes": 2}},
                                            {"timestamp": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                             "start": datetime(2011, 5, 19, tzinfo=timezone.utc),
                                             "end": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                             "resources": {"hours": 5, "minutes": 1}}])
        ms.store_allocation_usage(allocation_usage)
        updated_data = {"timestamp": datetime(2011, 5, 29, tzinfo=timezone.utc),
                        "start": datetime(2011, 5, 27, tzinfo=timezone.utc),
                        "end": datetime(2011, 5, 29, tzinfo=timezone.utc),
                        "resources": {"hours": 14, "minutes": 1}}
        result = ms.update_usage_in_allocation_usages("update_test_name", updated_data)
        self.assertEqual(allocation_usage.name, result)

    def test_remove_usage_in_allocation_usages(self):
        ms = MongoStorage()
        allocation_usage = AllocationUsage("plggtraining",
                                           {"last_update": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                            "resources": {"hours": 10}},
                                           [{"timestamp": datetime(2011, 5, 18, tzinfo=timezone.utc),
                                             "start": datetime(2011, 5, 15, tzinfo=timezone.utc),
                                             "end": datetime(2011, 5, 18, tzinfo=timezone.utc),
                                             "resources": {"hours": 4.5}},
                                            {"timestamp": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                             "start": datetime(2011, 5, 19, tzinfo=timezone.utc),
                                             "end": datetime(2011, 5, 20, tzinfo=timezone.utc),
                                             "resources": {"hours": 5.5}}])
        ms.store_allocation_usage(allocation_usage)

        result = ms.remove_usage_in_allocation_usages("remove_test_name", datetime(2011, 5, 10, tzinfo=timezone.utc),
                                                      datetime(2011, 5, 19, tzinfo=timezone.utc))
