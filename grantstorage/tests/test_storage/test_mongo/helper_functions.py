# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from grantstorage.storage.mongo.mongostorage import *
from grantstorage.localmodels.user import *
from grantstorage.localmodels.group import *
from grantstorage.localmodels.grant import *


# single create and store
def create_and_store_user(login, email, status, first_name, last_name, opi, affiliations):
    user = User(login, email, status, first_name, last_name, opi, affiliations)
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


def create_and_store_allocation_usage(name, summary, usages):
    allocation_usage = AllocationUsage(name, summary, usages)
    ms = MongoStorage()
    ms.store_allocation_usage(allocation_usage)
    return allocation_usage, ms


# many create and store
def create_and_store_many_users(logins, emails, statuses, first_names, last_names, opis, affiliations):
    users = []
    for i in range(len(logins)):
        users.append(User(logins[i], emails[i], statuses[i], first_names[i], last_names[i], opis[i], affiliations[i]))
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
