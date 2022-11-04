from pymongo import MongoClient
from datetime import datetime
from grantstorage.storage.mongo.mongostorage import *
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
