from grantstorage.storage.mongo.mongostorage import MongoStorage


class UserServicesController:
    def user_grant_info(self, login):
        mongo_storage = MongoStorage()
        groups = mongo_storage.find_groups_by_member(login)
        grants_dict = {}
        for group in groups:
            grants = mongo_storage.find_grants_by_group(group.name)
            for k in grants:
                grants_dict[k] = group
        return grants_dict

    def user_allocation_info(self, login):
        mongo_storage = MongoStorage()
        groups = mongo_storage.find_groups_by_member(login)
        allocations = {}
        for group in groups:
            allocation = mongo_storage.find_allocations_by_group(group.name)
            allocations[group] = allocation
        return allocations
