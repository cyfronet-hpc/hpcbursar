# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from .helper_functions import *
from datetime import date

"""
What to expect:
 - there will be 2 groups: group5, group6, group7
 - there will be 2 grants: grant5, grant6, grant7
"""


class TestMongoStorageSpecificFinds(TestCase):
    def test_find_groups_by_member(self):
        names = ["group5", "group6"]
        statuses = ["ACCEPTED", "ACCEPTED"]
        members = [["user3", "user4", "user5"], ["user1", "user5"]]
        leaders = [["user4"], ["user1", "user5"]]
        groups, ms = create_and_store_many_groups(names, statuses, members, leaders)

        groups_by_member = ms.find_groups_by_member("user5")
        for i in range(len(groups_by_member)):
            self.assertEqual(groups_by_member[i].name, groups[i].name)
            self.assertEqual(groups_by_member[i].status, groups[i].status)
            self.assertEqual(groups_by_member[i].members, groups[i].members)
            self.assertEqual(groups_by_member[i].leaders, groups[i].leaders)

    def test_find_grants_by_group(self):
        names = ["grant5", "grant6"]
        groups = ["group5", "group6"]
        statuses = ["ACTIVE", "INACTIVE"]
        starts = [date(2020, 12, 1), date(2019, 6, 15)]
        ends = [date(2020, 12, 31), date(2019, 7, 28)]
        allocations = [[Allocation("allocation5", "CPU", {"timelimit": 2, "hours": 4})],
                       [Allocation("allocation6", "GPU", {"timelimit": 10, "hours": 100})]]
        grants, ms = create_and_store_many_grants(names, groups, statuses, starts, ends, allocations)

        grants_by_group = ms.find_grants_by_group("group5")
        for i in range(len(grants_by_group)):
            self.assertEqual(grants_by_group[i].name, grants[i].name)
            self.assertEqual(grants_by_group[i].group, grants[i].group)
            self.assertEqual(grants_by_group[i].status, grants[i].status)
            self.assertEqual(grants_by_group[i].start, grants[i].start)
            self.assertEqual(grants_by_group[i].end, grants[i].end)
            for j in range(len(grants_by_group[i].allocations)):
                self.assertEqual(grants_by_group[i].allocations[j].name, grants[i].allocations[j].name)
                self.assertEqual(grants_by_group[i].allocations[j].resource, grants[i].allocations[j].resource)
                self.assertEqual(grants_by_group[i].allocations[j].parameters, grants[i].allocations[j].parameters)

    def test_find_allocations_by_group(self):
        name = "grant7"
        group = "group7"
        status = "ACTIVE"
        start = date(2024, 12, 1)
        end = date(2024, 12, 31)
        allocations = [Allocation("allocation7", "CPU", {"timelimit": 2, "hours": 4}),
                       Allocation("allocation8", "MEMORY", {"timelimit": 10, "hours": 3}),
                       Allocation("allocation9", "GPU", {"timelimit": 4, "hours": 6})]
        grant, ms = create_and_store_grant(name, group, status, start, end, allocations)

        allocations_by_group = ms.find_allocations_by_group("group7")

        for i in range(len(allocations_by_group)):
            for j in range(len(allocations_by_group[i])):
                self.assertEqual(allocations_by_group[i][j].name, allocations[j].name)
                self.assertEqual(allocations_by_group[i][j].resource, allocations[j].resource)
                self.assertEqual(allocations_by_group[i][j].parameters, allocations[j].parameters)
