# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from .helper_functions import *
from datetime import date

"""
What to expect:
 - there will be 2 users: user2, user3
 - there will be 2 groups: group2, group3
 - there will be 2 grants: grant2, grant3
 - there will be 2 allocation usages: allocation_usage2, allocation_usage3
"""


class TestMongoStorageManyStores(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_store_many_users(self):
        db = self.get_db()
        logins = ["user2", "user3"]
        emails = ["user2@cyfronet.pl", "user3@cyfronet.pl"]
        statuses = ["ACTIVE", "INACTIVE"]
        first_names = ["User", "User"]
        last_names = ["2", "3"]
        opis = ["", ""]
        affiliations = [
            [Affiliation("ACADEMIC_UNIT_EMPLOYEE", ["Uniwersytet Warszawski", "Wydział Matematyki"],
                         "ACTIVE", date(2023, 6, 30))],
            [Affiliation("ACADEMIC_EMPLOYEE", ["Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
                                               "Akademickie Centrum Komputerowe Cyfronet AGH"],
                         "INACTIVE", date(2025, 12, 31))]]
        users, _ = create_and_store_many_users(logins, emails, statuses, first_names, last_names, opis, affiliations)
        for i in range(len(users)):
            result = db["user"].find_one({"login": users[i].login})
            self.assertEqual(result["login"], users[i].login)
            self.assertEqual(result["email"], users[i].email)
            self.assertEqual(result["status"], users[i].status)
            self.assertEqual(result["first_name"], users[i].first_name)
            self.assertEqual(result["last_name"], users[i].last_name)
            self.assertEqual(result["opi"], users[i].opi)
            for j in range(len(users[i].affiliations)):
                self.assertEqual(result["affiliations"][j]["type"], users[i].affiliations[j].type)
                self.assertEqual(result["affiliations"][j]["units"], users[i].affiliations[j].units)
                self.assertEqual(result["affiliations"][j]["status"], users[i].affiliations[j].status)
                self.assertEqual(result["affiliations"][j]["end"], users[i].affiliations[j].end.isoformat())

    def test_store_many_groups(self):
        db = self.get_db()
        names = ["group2", "group3"]
        statuses = ["ACCEPTED", "PENDING"]
        members = [["user1", "user2"], ["user2", "user3"]]
        leaders = [["user2"], ["user3"]]
        groups, _ = create_and_store_many_groups(names, statuses, members, leaders)
        for i in range(len(groups)):
            result = db["group"].find_one({"name": groups[i].name})
            self.assertEqual(result["name"], groups[i].name)
            self.assertEqual(result["status"], groups[i].status)
            self.assertEqual(result["members"], groups[i].members)
            self.assertEqual(result["leaders"], groups[i].leaders)

    def test_store_many_grants(self):
        db = self.get_db()
        names = ["grant2", "grant3"]
        groups = ["group2", "group3"]
        statuses = ["ACTIVE", "INACTIVE"]
        starts = [date(2022, 7, 19), date(2019, 1, 7)]
        ends = [date(2022, 9, 19), date(2020, 1, 7)]
        allocations = [[Allocation("allocation2", "CPU", {"timelimit": 12, "hours": 24})],
                       [Allocation("allocation3", "GPU", {"timelimit": 100, "hours": 500})]]
        grants, _ = create_and_store_many_grants(names, groups, statuses, starts, ends, allocations)
        for i in range(len(grants)):
            result = db["grant"].find_one({"name": grants[i].name})
            self.assertEqual(result["name"], grants[i].name)
            self.assertEqual(result["group"], grants[i].group)
            self.assertEqual(result["status"], grants[i].status)
            self.assertEqual(result["start"], grants[i].start.isoformat())
            self.assertEqual(result["end"], grants[i].end.isoformat())
            for j in range(len(result["allocations"])):
                self.assertEqual(result["allocations"][j]["name"], grants[i].allocations[j].name)
                self.assertEqual(result["allocations"][j]["resource"], grants[i].allocations[j].resource)
                self.assertEqual(result["allocations"][j]["parameters"], grants[i].allocations[j].parameters)

    def test_store_many_allocation_usages(self):
        db = self.get_db()
        names = ["allocation_usage2", "allocation_usage3"]
        summaries = [Summary(datetime(2020, 4, 29), {"hours": 1, "minutes": 50}),
                     Summary(datetime(2022, 6, 20), {"minutes": 50})]
        usages = [
            [Usage(datetime(2020, 4, 15), datetime(2020, 4, 10), datetime(2020, 4, 14), {"hours": 1, "minutes": 45}),
             Usage(datetime(2020, 4, 29), datetime(2020, 4, 25), datetime(2020, 4, 25), {"minutes": 5})],
            [Usage(datetime(2022, 6, 20), datetime(2022, 6, 18), datetime(2022, 6, 19), {"minutes": 50})]]
        allocation_usages, _ = create_and_store_many_allocation_usages(names, summaries, usages)
        for i in range(len(allocation_usages)):
            result = db["allocation_usage"].find_one({"name": allocation_usages[i].name})
            self.assertEqual(result["name"], allocation_usages[i].name)
            self.assertEqual(result["summary"]["timestamp"],
                             allocation_usages[i].summary.timestamp.isoformat())
            self.assertEqual(result["summary"]["resources"], allocation_usages[i].summary.resources)
            for j in range(len(allocation_usages[i].usages)):
                self.assertEqual(result["usages"][j]["timestamp"], allocation_usages[i].usages[j].timestamp.isoformat())
                self.assertEqual(result["usages"][j]["start"], allocation_usages[i].usages[j].start.isoformat())
                self.assertEqual(result["usages"][j]["end"], allocation_usages[i].usages[j].end.isoformat())
                self.assertEqual(result["usages"][j]["resources"], allocation_usages[i].usages[j].resources)
