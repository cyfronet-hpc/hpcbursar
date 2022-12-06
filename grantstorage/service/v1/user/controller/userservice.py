# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from grantstorage.storage.mongo.mongostorage import MongoStorage


class UserServicesController:
    def user_grant_info(self, login):
        mongo_storage = MongoStorage()
        groups = mongo_storage.find_groups_by_member(login)
        grants_dict = {}
        for group in groups:
            grants = mongo_storage.find_grants_by_group(group.name)
            for grant in grants:
                allocation_usages = []
                for allocation in grant.allocations:
                    allocation_usage = mongo_storage.find_allocation_usage_by_name(allocation.name)
                    if allocation_usage:
                        allocation_usage += [allocation_usage]
                grants_dict[grant] = (group, allocation_usages)
        return grants_dict

    # def user_allocation_info(self, login):
    #     mongo_storage = MongoStorage()
    #     groups = mongo_storage.find_groups_by_member(login)
    #     allocations = {}
    #     for group in groups:
    #         allocation = mongo_storage.find_allocation_usages_by_name(group.name)
    #         allocations[group] = allocation
    #     return allocations
