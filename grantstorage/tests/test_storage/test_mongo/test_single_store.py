# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from datetime import date
from .helper_functions import *

"""
What to expect:
 - there will be 1 user: user1
 - there will be 1 group: group1
 - there will be 1 grant: grant1
 - there will be 1 allocation usage: allocation_usage1 
"""


class TestMongoStorageSingleStore(TestCase):
    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def test_store_user(self):
        db = self.get_db()
        affiliations = [Affiliation("ACADEMIC_UNIT_EMPLOYEE", ["Akademickie Centrum Komputerowe Cyfronet AGH"],
                                    "ACTIVE", date(2023, 12, 31))]
        user, _ = create_and_store_user("user1", "user1@cyfronet.pl", "ACTIVE", "User", "1", "", affiliations)

        result = db["user"].find_one({"login": user.login})
        self.assertEqual(result["login"], user.login)
        self.assertEqual(result["email"], user.email)
        self.assertEqual(result["status"], user.status)
        self.assertEqual(result["first_name"], user.first_name)
        self.assertEqual(result["last_name"], user.last_name)
        self.assertEqual(result["opi"], user.opi)
        for i in range(len(result["affiliations"])):
            self.assertEqual(result["affiliations"][i]["type"], user.affiliations[i].type)
            self.assertEqual(result["affiliations"][i]["units"], user.affiliations[i].units)
            self.assertEqual(result["affiliations"][i]["status"], user.affiliations[i].status)
            self.assertEqual(result["affiliations"][i]["end"], user.affiliations[i].end.isoformat())

    def test_store_group(self):
        db = self.get_db()
        group, _ = create_and_store_group("group1", "ACCEPTED", ["user1"], ["user1"])

        result = db["group"].find_one({"name": group.name})
        self.assertEqual(result["name"], group.name)
        self.assertEqual(result["status"], group.status)
        self.assertEqual(result["members"], group.members)
        self.assertEqual(result["leaders"], group.leaders)

    def test_store_grant(self):
        db = self.get_db()
        allocation = [Allocation("allocation1", "CPU", {"timelimit": 72, "hours": 10000000})]
        grant, _ = create_and_store_grant("grant1", "group1", "ACTIVE", date(2021, 5, 8), date(2022, 5, 1),
                                          allocation)

        result = db["grant"].find_one({"name": grant.name})
        self.assertEqual(result["name"], grant.name)
        self.assertEqual(result["group"], grant.group)
        self.assertEqual(result["status"], grant.status)
        self.assertEqual(result["start"], grant.start.isoformat())
        self.assertEqual(result["end"], grant.end.isoformat())
        for i in range(len(result["allocations"])):
            self.assertEqual(result["allocations"][i]["name"], grant.allocations[i].name)
            self.assertEqual(result["allocations"][i]["resource"], grant.allocations[i].resource)
            self.assertEqual(result["allocations"][i]["parameters"], grant.allocations[i].parameters)

    def test_store_allocation_usage(self):
        db = self.get_db()
        summary = Summary(datetime(2020, 5, 17), {"hours": 4, "minutes": 5})
        usages = [Usage(datetime(2020, 5, 1), datetime(2020, 5, 15), datetime(2020, 5, 16), {"hours": 3, "minutes": 6})]
        allocation_usage, _ = create_and_store_allocation_usage("allocation_usage1", summary, usages)

        result = db["allocation_usage"].find_one({"name": allocation_usage.name})
        self.assertEqual(result["name"], allocation_usage.name)
        self.assertEqual(result["summary"]["timestamp"], allocation_usage.summary.timestamp.isoformat())
        self.assertEqual(result["summary"]["resources"], allocation_usage.summary.resources)
        for i in range(len(result["usages"])):
            self.assertEqual(result["usages"][i]["timestamp"],
                             allocation_usage.usages[i].timestamp.isoformat())
            self.assertEqual(result["usages"][i]["start"], allocation_usage.usages[i].start.isoformat())
            self.assertEqual(result["usages"][i]["end"], allocation_usage.usages[i].end.isoformat())
            self.assertEqual(result["usages"][i]["resources"], allocation_usage.usages[i].resources)
