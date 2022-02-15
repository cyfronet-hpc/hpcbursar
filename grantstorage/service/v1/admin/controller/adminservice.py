from grantstorage.storage.mongo.mongostorage import MongoStorage


class AdminServicesController:
    def grant_group_info(self):
        mongo_storage = MongoStorage()
        groups = mongo_storage.find_all_groups()
        grants = mongo_storage.find_all_grants()
        return grants, groups
