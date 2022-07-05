from django.test import TestCase
from grantstorage.storage.mongo.mongostorage import *
from pymongo import MongoClient
from datetime import datetime
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

    # TODO repair test_store_grant NOT WORKING
    def test_store_grant(self):
        db = self.get_db()
        # Create a new grant
        name = "test_grant"
        group = "test_group"
        status = "grant_active"
        start = "2021-05-08"
        end = "2022-05-10"
        allocations = Allocation("test_allocation", "CPU", {"timelimit": 72, "hours": 10000000})
        grant = Grant(name, group, status, start, end, allocations)

        # Add grant to the database
        ms = MongoStorage()
        ms.store_grant(grant)

        result = db["grant"].find_one(
            {"name": name, "group": group, "status": status, "start": start, "end": end, "allocations": allocations})
        self.assertEqual(result["name"], grant.name)
        self.assertEqual(result["group"], grant.group)
        self.assertEqual(result["status"], grant.status)
        self.assertEqual(result["start"], grant.start)
        self.assertEqual(result["end"], grant.end)
        self.assertEqual(result["allocations"], grant.allocations)

    # TODO repair test_store_allocation_usage NOT WORKING
    def test_store_allocation_usage(self):
        db = self.get_db()
        # Create new allocation usage
        name = "test_name"
        summary = Summary(datetime(2020, 5, 17), {"hours": 4, "minutes": 5})
        usage = Usage(datetime(2020, 5, 17), datetime(2020, 5, 15), datetime(2020, 5, 16), {"hours": 15, "minutes": 6})
        allocation_usage = AllocationUsage(name, summary, usage)

        # Add allocation_usage to the database
        ms = MongoStorage()
        ms.store_allocation_usage(allocation_usage)

        result = db["allocation_usages"].find_one({"name": name, "summary": summary, "usage": usage})
        self.assertEqual(result["name"], allocation_usage.name)
        self.assertEqual(result["summary"], allocation_usage.summary)
        self.assertEqual(result["usage"], allocation_usage.usage)


class TestMongoStorageSingleFind(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_find_user_by_login(self):
        # Create a new user
        login = "test_user"
        status = "ACTIVE"
        user = User(login, status)

        # Add user to the database
        ms = MongoStorage()
        ms.store_user(user)

        self.assertEqual(ms.find_user_by_login(login).login, user.login)
        self.assertEqual(ms.find_user_by_login(login).status, user.status)

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

        self.assertEqual(ms.find_group_by_name(name).name, group.name)
        self.assertEqual(ms.find_group_by_name(name).status, group.status)
        self.assertEqual(ms.find_group_by_name(name).members, group.members)
        self.assertEqual(ms.find_group_by_name(name).leaders, group.leaders)

    # TODO repair test_find_grant_by_name NOT WORKING
    def test_find_grant_by_name(self):
        # Create a new grant
        name = "test_grant"
        group = "test_group"
        status = "grant_active"
        start = "2021-05-08"
        end = "2022-05-07"
        allocations = Allocation("test_allocation", "CPU", {"timelimit": 72, "hours": 10000000})
        grant = Grant(name, group, status, start, end, allocations)

        # Add grant to the database
        ms = MongoStorage()
        ms.store_grant(grant)

        self.assertEqual(ms.find_grant_by_name(name).name, grant.name)
        self.assertEqual(ms.find_grant_by_name(name).group, grant.group)
        self.assertEqual(ms.find_grant_by_name(name).status, grant.status)
        self.assertEqual(ms.find_grant_by_name(name).start, grant.start)
        self.assertEqual(ms.find_grant_by_name(name).end, grant.end)

    def test_find_all_users(self):
        pass

    def test_find_all_group(self):
        pass

    def test_find_all_grants(self):
        pass


class TestMongoStorageSpecificFinds(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_find_groups_by_member(self):
        pass

    def test_find_grants_by_group(self):
        ms = MongoStorage()
        # Create some grants
        grant_1 = Grant("test_grant_1", "test_group", "grant_active", "2021-05-08", "2022-05-10",
                        [{"name": "test-storage-1", "resource": "Storage", "parameters": {"capacity": 1000}},
                         {"name": "test-cpu-1", "resource": "CPU", "parameters": {"timelimit": 168, "hours": 200000}}])
        ms.store_grant(grant_1)

        grant_2 = Grant("test_grant_2", "test_group", "grant_active", "2021-10-11", "2022-10-15",
                        [{"name": "test-storage-2", "resource": "Storage", "parameters": {"capacity": 100}},
                         {"name": "test-cpu-2", "resource": "GPU", "parameters": {"timelimit": 10, "hours": 200}}])
        ms.store_grant(grant_2)

        # Create group
        group = Group("test_group", "ACTIVE", ["user1", "user2", "user3"], ["user1"])
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
        # Create some allocation usages
        allocation_usage = AllocationUsage("test_name",
                                           {"last_update": datetime(2020, 5, 7),
                                            "resources": {"hours": 10, "minutes": 3}},
                                           [{"timestamp": datetime(2020, 5, 5, tzinfo=None),
                                             "start": datetime(2020, 5, 4, tzinfo=None),
                                             "end": datetime(2020, 5, 5), "resources": {"hours": 4, "minutes": 2}},
                                            {"timestamp": datetime(2020, 5, 6), "start": datetime(2020, 5, 5),
                                             "end": datetime(2020, 5, 6), "resources": {"hours": 6, "minutes": 1}}])
        ms.store_allocation_usage(allocation_usage)

        result = ms.find_allocation_usages_by_name("test_name")
        self.assertEqual(result[0].name, allocation_usage.name)
        # print(dict(result[0].summary)["last_update"])
        # print(allocation_usage.summary["last_update"])
        # self.assertEqual(dict(result[0].summary), allocation_usage.summary)
        # self.assertEqual(dict(result[0].usage), allocation_usage.usage)

    def test_find_allocations_by_group(self):
        pass

    def test_update_usage_in_allocation_usages(self):
        pass

    def test_remove_usage_in_allocation_usages(self):
        pass
