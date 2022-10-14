# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.storage.mongo.mongostorage import *
from pymongo import MongoClient
from datetime import datetime
from grantstorage.localmodels.user import *
from grantstorage.localmodels.group import *
from grantstorage.localmodels.grant import *


# single create and store
def create_and_store_user(login, status):
    user = User(login, status)
    ms = MongoStorage()
    ms.store_user(user)
    return user, ms


def create_and_store_group(name, status, members, leaders):
    group = Group(name, status, members, leaders)
    ms = MongoStorage()
    ms.store_group(group)
    return group, ms


def create_and_store_grant(name, group, status, start, end, allocations):
    grant = Grant(name, group, status, start, end, allocations)
    ms = MongoStorage()
    ms.store_grant(grant)
    return grant, ms


def create_and_store_allocation_usage(name, summary, usage):
    allocation_usage = AllocationUsage(name, summary, usage)
    ms = MongoStorage()
    ms.store_allocation_usage(allocation_usage)
    return allocation_usage, ms


# many create and store
def create_and_store_many_users(logins, statuses):
    users = []
    for i in range(len(logins)):
        users.append(User(logins[i], statuses[i]))
    ms = MongoStorage()
    ms.store_users(users)
    return users, ms


def create_and_store_many_groups(names, statuses, members, leaders):
    groups = []
    for i in range(len(names)):
        groups.append(Group(names[i], statuses[i], members[i], leaders[i]))
    ms = MongoStorage()
    ms.store_groups(groups)
    return groups, ms


def create_and_store_many_grants(names, groups, statuses, starts, ends, allocations):
    grants = []
    for i in range(len(names)):
        grants.append(Grant(names[i], groups[i], statuses[i], starts[i], ends[i], allocations[i]))
    ms = MongoStorage()
    ms.store_grants(grants)
    return grants, ms


def create_and_store_many_allocation_usages(names, summaries, usages):
    allocation_usages = []
    for i in range(len(names)):
        allocation_usages.append(AllocationUsage(names[i], summaries[i], usages[i]))
    ms = MongoStorage()
    ms.store_allocation_usages(allocation_usages)
    return allocation_usages, ms


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
        user, _ = create_and_store_user("user1", "ACTIVE")

        result = db["user"].find_one({"login": user.login})
        self.assertEqual(result["login"], user.login)
        self.assertEqual(result["status"], user.status)

    def test_store_group(self):
        db = self.get_db()
        group, _ = create_and_store_group("group1", "ACCEPTED", ["user1", "user2", "user3"], ["user1", "user2"])

        result = db["group"].find_one({"name": group.name})
        self.assertEqual(result["name"], group.name)
        self.assertEqual(result["status"], group.status)
        self.assertEqual(result["members"], group.members)
        self.assertEqual(result["leaders"], group.leaders)

    def test_store_grant(self):
        db = self.get_db()
        allocation = [Allocation("allocation1", "CPU", {"timelimit": 72, "hours": 10000000})]
        grant, _ = create_and_store_grant("grant1", "group1", "ACTIVE", "2021-05-08", "2022-05-10", allocation)

        result = db["grant"].find_one({"name": grant.name})
        self.assertEqual(result["name"], grant.name)
        self.assertEqual(result["group"], grant.group)
        self.assertEqual(result["status"], grant.status)
        self.assertEqual(result["start"], grant.start)
        self.assertEqual(result["end"], grant.end)
        for i in range(len(result["allocations"])):
            self.assertEqual(result["allocations"][i]["name"], grant.allocations[i].name)
            self.assertEqual(result["allocations"][i]["resource"], grant.allocations[i].resource)
            self.assertEqual(result["allocations"][i]["parameters"], grant.allocations[i].parameters)

    def test_store_allocation_usage(self):
        db = self.get_db()
        summary = Summary(datetime(2020, 5, 17), {"hours": 4, "minutes": 5})
        usage = [Usage(datetime(2020, 5, 17), datetime(2020, 5, 15), datetime(2020, 5, 16), {"hours": 3, "minutes": 6})]
        allocation_usage, _ = create_and_store_allocation_usage("allocation_usage1", summary, usage)

        result = db["allocation_usages"].find_one({"name": allocation_usage.name})
        self.assertEqual(result["name"], allocation_usage.name)
        self.assertEqual(result["summary"]["last_update"],
                         allocation_usage.summary.last_update.astimezone().isoformat())
        self.assertEqual(result["summary"]["resources"], allocation_usage.summary.resources)
        for i in range(len(result["usage"])):
            self.assertEqual(result["usage"][i]["timestamp"],
                             allocation_usage.usage[i].timestamp.astimezone().isoformat())
            self.assertEqual(result["usage"][i]["start"], allocation_usage.usage[i].start.astimezone().isoformat())
            self.assertEqual(result["usage"][i]["end"], allocation_usage.usage[i].end.astimezone().isoformat())
            self.assertEqual(result["usage"][i]["resources"], allocation_usage.usage[i].resources)


class TestMongoStorageManyStores(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_store_many_users(self):
        db = self.get_db()
        logins = ["user2", "user3"]
        statuses = ["ACTIVE", "INACTIVE"]
        users, _ = create_and_store_many_users(logins, statuses)
        for i in range(len(users)):
            result = db["user"].find_one({"login": users[i].login})
            self.assertEqual(result["login"], users[i].login)
            self.assertEqual(result["status"], users[i].status)

    def test_store_many_groups(self):
        db = self.get_db()
        names = ["group2", "group3"]
        statuses = ["ACCEPTED", "PENDING"]
        members = [["user3", "user4"], ["user2", "user3", "user5"]]
        leaders = [["user3"], ["user2", "user5"]]
        groups, _ = create_and_store_many_groups(names, statuses, members, leaders)
        for i in range(len(groups)):
            result = db["group"].find_one({"name": groups[i].name})
            self.assertEqual(result["name"], groups[i].name)
            self.assertEqual(result["status"], groups[i].status)
            self.assertEqual(result["members"], groups[i].members)
            self.assertEqual(result["leaders"], groups[i].leaders)

    def test_store_many_grants(self):
        db = self.get_db()
        names = ["grant1", "grant2"]
        groups = ["group1", "group2"]
        statuses = ["ACTIVE", "INACTIVE"]
        starts = ["2022-07-19", "2019-01-07"]
        ends = ["2022-09-19", "2020-01-07"]
        allocations = [[Allocation("allocation1", "CPU", {"timelimit": 12, "hours": 24})],
                       [Allocation("allocation2", "GPU", {"timelimit": 100, "hours": 500})]]
        grants, _ = create_and_store_many_grants(names, groups, statuses, starts, ends, allocations)
        for i in range(len(grants)):
            result = db["grant"].find_one({"name": grants[i].name})
            self.assertEqual(result["name"], grants[i].name)
            self.assertEqual(result["group"], grants[i].group)
            self.assertEqual(result["status"], grants[i].status)
            self.assertEqual(result["start"], grants[i].start)
            self.assertEqual(result["end"], grants[i].end)
            for j in range(len(result["allocations"])):
                self.assertEqual(result["allocations"][j]["name"], grants[i].allocations[j].name)
                self.assertEqual(result["allocations"][j]["resource"], grants[i].allocations[j].resource)
                self.assertEqual(result["allocations"][j]["parameters"], grants[i].allocations[j].parameters)

    def test_store_many_allocation_usages(self):
        db = self.get_db()
        names = ["name1", "name2"]
        summaries = [Summary(datetime(2020, 4, 29), {"hours": 1, "minutes": 50}),
                     Summary(datetime(2022, 6, 20), {"minutes": 50})]
        usages = [
            [Usage(datetime(2020, 4, 15), datetime(2020, 4, 10), datetime(2020, 4, 14), {"hours": 1, "minutes": 45}),
             Usage(datetime(2020, 4, 29), datetime(2020, 4, 25), datetime(2020, 4, 25), {"minutes": 5})],
            [Usage(datetime(2022, 6, 20), datetime(2022, 6, 18), datetime(2022, 6, 19), {"minutes": 50})]]
        allocation_usages, _ = create_and_store_many_allocation_usages(names, summaries, usages)
        for i in range(len(allocation_usages)):
            result = db["allocation_usages"].find_one({"name": allocation_usages[i].name})
            self.assertEqual(result["name"], allocation_usages[i].name)
            self.assertEqual(result["summary"]["last_update"],
                             allocation_usages[i].summary.last_update.astimezone().isoformat())
            self.assertEqual(result["summary"]["resources"], allocation_usages[i].summary.resources)
            for j in range(len(allocation_usages[i].usage)):
                self.assertEqual(result["usage"][j]["timestamp"],
                                 allocation_usages[i].usage[j].timestamp.astimezone().isoformat())
                self.assertEqual(result["usage"][j]["start"],
                                 allocation_usages[i].usage[j].start.astimezone().isoformat())
                self.assertEqual(result["usage"][j]["end"], allocation_usages[i].usage[j].end.astimezone().isoformat())
                self.assertEqual(result["usage"][j]["resources"], allocation_usages[i].usage[j].resources)


class TestMongoStorageSingleFind(TestCase):
    def test_find_user_by_login(self):
        user, ms = create_and_store_user("test_user", "ACTIVE")

        result = ms.find_user_by_login(user.login)
        self.assertEqual(result.login, user.login)
        self.assertEqual(result.status, user.status)

    def test_find_group_by_name(self):
        group, ms = create_and_store_group("test_name", "ACCEPTED", ["user1", "user2", "user3"], ["test_user", "user1"])

        result = ms.find_group_by_name(group.name)
        self.assertEqual(result.name, group.name)
        self.assertEqual(result.status, group.status)
        self.assertEqual(result.members, group.members)
        self.assertEqual(result.leaders, group.leaders)

    def test_find_grant_by_name(self):
        allocation = [Allocation("test_allocation", "CPU", {"timelimit": 72, "hours": 10000000})]
        grant, ms = create_and_store_grant("test_grant", "test_group", "ACTIVE", "2021-05-08", "2022-05-07", allocation)

        result = ms.find_grant_by_name(grant.name)
        self.assertEqual(result.name, grant.name)
        self.assertEqual(result.group, grant.group)
        self.assertEqual(result.status, grant.status)
        self.assertEqual(str(result.start), grant.start)
        self.assertEqual(str(result.end), grant.end)
        for i in range(len(result.allocations)):
            self.assertEqual(result.allocations[i].name, grant.allocations[i].name)
            self.assertEqual(result.allocations[i].resource, grant.allocations[i].resource)
            self.assertEqual(result.allocations[i].parameters, grant.allocations[i].parameters)


# TODO start from here
class TestMongoStorageSpecificFinds(TestCase):
    def test_find_groups_by_member(self):
        names = ["group1", "group2"]
        statuses = ["ACCEPTED", "PENDING"]
        members = [["user1", "user2"], ["user2", "user3", "user4"]]
        leaders = [["user1"], ["user3", "user5"]]
        groups, ms = create_and_store_many_groups(names, statuses, members, leaders)

        user_groups = ms.find_groups_by_member("user2")
        for i in range(len(user_groups)):
            self.assertEqual(user_groups[i].name, groups[i].name)
            self.assertEqual(user_groups[i].status, groups[i].status)
            self.assertEqual(user_groups[i].members, groups[i].members)
            self.assertEqual(user_groups[i].leaders, groups[i].leaders)

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
