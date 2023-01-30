# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from grantstorage.storage.mongo.mongostorage import MongoStorage


class AdminServicesController:
    mongo_storage = MongoStorage()

    def grant_group_info(self):
        groups = self.mongo_storage.find_all_groups()
        grants = self.mongo_storage.find_all_grants()
        return grants, groups

    def grant_info(self, name):
        return self.mongo_storage.find_grant_by_name(name)

    def group_info(self, name):
        return self.mongo_storage.find_group_by_name(name)

    def user_info(self, login):
        return self.mongo_storage.find_user_by_login(login)

    def allocation_usage_info(self, name):
        return self.mongo_storage.find_allocation_usage_by_name(name)
