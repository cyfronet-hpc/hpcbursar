# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.storage.mongo.mongostorage import *
from pymongo import MongoClient
from datetime import datetime, timezone
from grantstorage.localmodels.user import *
from grantstorage.localmodels.group import *
from grantstorage.localmodels.grant import *


class TestMongoStorageExpectedValues(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_expected_collections(self):
        db = self.get_db()
        collections = db.list_collection_names()
        expected_collections = ["group", "user", "grant", "allocation_usages"]
        for col in collections:
            self.assertIn(col, expected_collections)


class TestMongoStorageSingleStore(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_store_user(self):
        db = self.get_db()
        # Create a new user
        login = "test_user"
        status = "ACTIVE"
        user = User(login, status)

        # Add user to the database
        ms = MongoStorage()
        ms.store_user(user)

        result = db["user"].find_one({"login": login, "status": status})
        self.assertEqual(result["login"], user.login)
        self.assertEqual(result["status"], user.status)

    def test_store_group(self):
        db = self.get_db()
        # Create a new group
        name = "test_name"
        status = "ACCEPTED"
        members = ["user1", "user2", "user3"]
        leaders = ["user1", "user2"]
        group = Group(name, status, members, leaders)

        # Add group to the database
        ms = MongoStorage()
        ms.store_group(group)

        result = db["group"].find_one({"name": name, "status": status, "members": members, "leaders": leaders})
        self.assertEqual(result["name"], group.name)
        self.assertEqual(result["status"], group.status)
        self.assertEqual(result["members"], group.members)
        self.assertEqual(result["leaders"], group.leaders)

    def test_store_grant(self):
        db = self.get_db()
        # Create a new grant
        name = "test_grant"
        group = "test_group"
        status = "grant_active"
        start = "2021-05-08"
        end = "2022-05-10"
        allocations = Allocation("test_allocation", "CPU", {"timelimit": 72, "hours": 10000000})
        grant = Grant(name, group, status, start, end, [allocations])

        # Add grant to the database
        ms = MongoStorage()
        ms.store_grant(grant)

        result = db["grant"].find_one(
            {"name": name, "group": group, "status": status, "start": start, "end": end})
        self.assertEqual(result["name"], grant.name)
        self.assertEqual(result["group"], grant.group)
        self.assertEqual(result["status"], grant.status)
        self.assertEqual(result["start"], grant.start)
        self.assertEqual(result["end"], grant.end)
        self.assertEqual(result["allocations"][0]["name"], grant.allocations[0].name)
        self.assertEqual(result["allocations"][0]["resource"], grant.allocations[0].resource)
        self.assertEqual(result["allocations"][0]["parameters"], grant.allocations[0].parameters)

    def test_store_allocation_usage(self):
        db = self.get_db()
        # Create new allocation usage
        name = "test_name"
        summary = Summary(datetime(2020, 5, 17), {"hours": 4, "minutes": 5})
        usage = Usage(datetime(2020, 5, 17), datetime(2020, 5, 15), datetime(2020, 5, 16), {"hours": 15, "minutes": 6})
        allocation_usage = AllocationUsage(name, summary, [usage])

        # Add allocation_usage to the database
        ms = MongoStorage()
        ms.store_allocation_usage(allocation_usage)

        result = db["allocation_usages"].find_one({"name": name})
        self.assertEqual(result["name"], allocation_usage.name)
        self.assertEqual(datetime.fromisoformat(result["summary"]["last_update"][:-1]),
                         allocation_usage.summary.last_update)
        self.assertEqual(result["summary"]["resources"], allocation_usage.summary.resources)
        self.assertEqual(datetime.fromisoformat(result["usage"][0]["timestamp"][:-1]),
                         allocation_usage.usage[0].timestamp)
        self.assertEqual(datetime.fromisoformat(result["usage"][0]["start"][:-1]), allocation_usage.usage[0].start)
        self.assertEqual(datetime.fromisoformat(result["usage"][0]["end"][:-1]), allocation_usage.usage[0].end)
        self.assertEqual(result["usage"][0]["resources"], allocation_usage.usage[0].resources)


class TestMongoStorageSingleFind(TestCase):
    def test_find_user_by_login(self):
        # Create a new user
        login = "test_user"
        status = "ACTIVE"
        user = User(login, status)

        # Add user to the database
        ms = MongoStorage()
        ms.store_user(user)

        result = ms.find_user_by_login(login)
        self.assertEqual(result.login, user.login)
        self.assertEqual(result.status, user.status)

    def test_find_group_by_name(self):
        # Create a new group
        name = "test_name"
        status = "ACCEPTED"
        members = ["user1", "user2", "user3"]
        leaders = ["test_user", "user1"]
        group = Group(name, status, members, leaders)

        # Add group to the database
        ms = MongoStorage()
        ms.store_group(group)

        result = ms.find_group_by_name(name)
        self.assertEqual(result.name, group.name)
        self.assertEqual(result.status, group.status)
        self.assertEqual(result.members, group.members)
        self.assertEqual(result.leaders, group.leaders)

    def test_find_grant_by_name(self):
        # Create a new grant
        name = "test_grant"
        group = "test_group"
        status = "grant_active"
        start = "2021-05-08"
        end = "2022-05-07"
        allocations = Allocation("test_allocation", "CPU", {"timelimit": 72, "hours": 10000000})
        grant = Grant(name, group, status, start, end, [allocations])

        # Add grant to the database
        ms = MongoStorage()
        ms.store_grant(grant)

        result = ms.find_grant_by_name(name)
        self.assertEqual(result.name, grant.name)
        self.assertEqual(result.group, grant.group)
        self.assertEqual(result.status, grant.status)
        self.assertEqual(str(result.start), grant.start)
        self.assertEqual(str(result.end), grant.end)
        self.assertEqual(result.allocations[0].name, grant.allocations[0].name)
        self.assertEqual(result.allocations[0].resource, grant.allocations[0].resource)
        self.assertEqual(result.allocations[0].parameters, grant.allocations[0].parameters)


class TestMongoStorageSpecificFinds(TestCase):
    def test_find_groups_by_member(self):
        ms = MongoStorage()
        # Create some groups
        name_1 = "test_group_1"
        status_1 = "ACCEPTED"
        members_1 = ["user_1", "user_2", "user_3"]
        leaders_1 = ["user_1", "user_3"]
        group_1 = Group(name_1, status_1, members_1, leaders_1)
        ms.store_group(group_1)

        name_2 = "test_group_2"
        status_2 = "ACCEPTED"
        members_2 = ["user_1", "user_3"]
        leaders_2 = ["user_1"]
        group_2 = Group(name_2, status_2, members_2, leaders_2)
        ms.store_group(group_2)

        user_1_groups = ms.find_groups_by_member("user_1")
        groups = [group_1, group_2]
        for i in range(len(user_1_groups)):
            self.assertEqual(user_1_groups[i].name, groups[i].name)
            self.assertEqual(user_1_groups[i].status, groups[i].status)
            self.assertEqual(user_1_groups[i].members, groups[i].members)
            self.assertEqual(user_1_groups[i].leaders, groups[i].leaders)

    def test_find_grants_by_group(self):
        ms = MongoStorage()
        # Create some grants
        grant_1 = Grant("test_grant_1", "new_test_group", "grant_active", "2021-05-08", "2022-05-10",
                        [{"name": "test-storage-1", "resource": "Storage", "parameters": {"capacity": 1000}},
                         {"name": "test-cpu-1", "resource": "CPU", "parameters": {"timelimit": 168, "hours": 200000}}])
        ms.store_grant(grant_1)

        grant_2 = Grant("test_grant_2", "new_test_group", "grant_active", "2021-10-11", "2022-10-15",
                        [{"name": "test-storage-2", "resource": "Storage", "parameters": {"capacity": 100}},
                         {"name": "test-cpu-2", "resource": "GPU", "parameters": {"timelimit": 10, "hours": 200}}])
        ms.store_grant(grant_2)

        # Create group
        group = Group("new_test_group", "ACTIVE", ["user1", "user2", "user3"], ["user1"])
        ms.store_group(group)

        result = ms.find_grants_by_group(group.name)
        grants = [grant_1, grant_2]
        for i in range(len(result)):
            self.assertEqual(result[i].name, grants[i].name)
            self.assertEqual(result[i].group, grants[i].group)
            self.assertEqual(result[i].status, grants[i].status)
            self.assertEqual(str(result[i].start), grants[i].start)
            self.assertEqual(str(result[i].end), grants[i].end)
            for j in range(len(grants[i].allocations)):
                self.assertEqual(result[i].allocations[j].name, grants[i].allocations[j]["name"])
                self.assertEqual(result[i].allocations[j].resource, grants[i].allocations[j]["resource"])
                self.assertEqual(result[i].allocations[j].parameters, grants[i].allocations[j]["parameters"])

    def test_find_allocation_usages_by_name(self):
        ms = MongoStorage()
        # Create allocation usage
        allocation_usage = AllocationUsage("test_name",
                                           {"last_update": datetime(2020, 5, 7, tzinfo=timezone.utc),
                                            "resources": {"hours": 10, "minutes": 3}},
                                           [{"timestamp": datetime(2020, 5, 5, tzinfo=timezone.utc),
                                             "start": datetime(2020, 5, 4, tzinfo=timezone.utc),
                                             "end": datetime(2020, 5, 5, tzinfo=timezone.utc),
                                             "resources": {"hours": 4, "minutes": 2}},
                                            {"timestamp": datetime(2020, 5, 6, tzinfo=timezone.utc),
                                             "start": datetime(2020, 5, 5, tzinfo=timezone.utc),
                                             "end": datetime(2020, 5, 6, tzinfo=timezone.utc),
                                             "resources": {"hours": 6, "minutes": 1}}])
        ms.store_allocation_usage(allocation_usage)

        result = ms.find_allocation_usages_by_name("test_name")
        self.assertEqual(result[0].name, allocation_usage.name)
        self.assertEqual(result[0].summary, allocation_usage.summary)
        for u in range(len(result[0].usage)):
            self.assertEqual(result[0].usage[u].timestamp, allocation_usage.usage[u]["timestamp"])
            self.assertEqual(result[0].usage[u].start, allocation_usage.usage[u]["start"])
            self.assertEqual(result[0].usage[u].end, allocation_usage.usage[u]["end"])
            self.assertEqual(result[0].usage[u].resources, allocation_usage.usage[u]["resources"])

    def test_find_allocations_by_group(self):
        ms = MongoStorage()
        # Create some allocation usages
        allocation_usage = AllocationUsage("test_name",
                                           {"last_update": datetime(2001, 5, 25, tzinfo=timezone.utc),
                                            "resources": {"hours": 10, "minutes": 3}},
                                           [{"timestamp": datetime(2001, 5, 11, tzinfo=timezone.utc),
                                             "start": datetime(2001, 5, 8, tzinfo=timezone.utc),
                                             "end": datetime(2001, 5, 10, tzinfo=timezone.utc),
                                             "resources": {"hours": 5, "minutes": 2}},
                                            {"timestamp": datetime(2001, 5, 25, tzinfo=timezone.utc),
                                             "start": datetime(2001, 5, 21, tzinfo=timezone.utc),
                                             "end": datetime(2001, 5, 24, tzinfo=timezone.utc),
                                             "resources": {"hours": 10, "minutes": 30}}])
        ms.store_allocation_usage(allocation_usage)

    # TODO: repair update usage, still not working
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

    # TODO: repair remove usage, still not working
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
