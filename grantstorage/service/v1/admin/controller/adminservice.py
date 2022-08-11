# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from grantstorage.storage.mongo.mongostorage import MongoStorage


class AdminServicesController:
    def grant_group_info(self):
        mongo_storage = MongoStorage()
        groups = mongo_storage.find_all_groups()
        grants = mongo_storage.find_all_grants()
        return grants, groups
