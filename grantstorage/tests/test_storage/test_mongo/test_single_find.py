# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from .helper_functions import *
from datetime import date

"""
What to expect:
 - there will be 1 user: user4
 - there will be 1 group: group4
 - there will be 1 grant: grant4
"""


class TestMongoStorageSingleFind(TestCase):
    def test_find_user_by_login(self):
        affiliations = [Affiliation("ACADEMIC_UNIT_EMPLOYEE", ["Uniwersytet Warszawski",
                                                               "Wydział Matematyki Informatyki i Mechaniki"],
                                    "ACTIVE", date(2023, 12, 31))]
        user, ms = create_and_store_user("user4", "user4@cyfronet.pl", "ACTIVE", "User", "4", "", affiliations)

        result = ms.find_user_by_login(user.login)
        self.assertEqual(result.login, user.login)
        self.assertEqual(result.email, user.email)
        self.assertEqual(result.status, user.status)
        self.assertEqual(result.first_name, user.first_name)
        self.assertEqual(result.last_name, user.last_name)
        self.assertEqual(result.opi, user.opi)
        for i in range(len(result.affiliations)):
            self.assertEqual(result.affiliations[i].type, user.affiliations[i].type)
            self.assertEqual(result.affiliations[i].units, user.affiliations[i].units)
            self.assertEqual(result.affiliations[i].status, user.affiliations[i].status)
            self.assertEqual(result.affiliations[i].end, user.affiliations[i].end)

    def test_find_group_by_name(self):
        group, ms = create_and_store_group("group4", "ACCEPTED", ["user2", "user3", "user4"], ["user2", "user4"])

        result = ms.find_group_by_name(group.name)
        self.assertEqual(result.name, group.name)
        self.assertEqual(result.status, group.status)
        self.assertEqual(result.members, group.members)
        self.assertEqual(result.leaders, group.leaders)

    def test_find_grant_by_name(self):
        allocation = [Allocation("allocation4", "CPU", {"timelimit": 72, "hours": 10000000})]
        grant, ms = create_and_store_grant("grant4", "group4", "ACTIVE", date(2021, 5, 8), date(2022, 5, 7), allocation)

        result = ms.find_grant_by_name(grant.name)
        self.assertEqual(result.name, grant.name)
        self.assertEqual(result.group, grant.group)
        self.assertEqual(result.status, grant.status)
        self.assertEqual(result.start, grant.start)
        self.assertEqual(result.end, grant.end)
        for i in range(len(result.allocations)):
            self.assertEqual(result.allocations[i].name, grant.allocations[i].name)
            self.assertEqual(result.allocations[i].resource, grant.allocations[i].resource)
            self.assertEqual(result.allocations[i].parameters, grant.allocations[i].parameters)
