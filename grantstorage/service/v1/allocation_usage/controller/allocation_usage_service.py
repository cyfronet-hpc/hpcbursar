from grantstorage.storage.mongo.mongostorage import MongoStorage


class AllocationUsageController:
    def user_allocation_info(self, login):
        mongo_storage = MongoStorage()
        allocations = mongo_storage.find_allocations_by_login(login)

