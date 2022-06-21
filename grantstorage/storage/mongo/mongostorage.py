from pymongo import MongoClient
from grantstorage.localmodels.user import User, UserSerializer
from grantstorage.localmodels.group import Group, GroupSerializer
from grantstorage.localmodels.grant import Grant, GrantSerializer
from grantstorage.localmodels.allocation_usage import *

MODEL_TYPE_TO_COLLECTION = {
    User: 'user',
    Group: 'group',
    Grant: 'grant',
    AllocationUsage: 'allocation_usages'
}

MODEL_TYPE_TO_SERIALIZER = {
    User: UserSerializer,
    Group: GroupSerializer,
    Grant: GrantSerializer,
    AllocationUsage: AllocationUsageSerializer
}

MODEL_TYPE_TO_NAMEFIELD = {
    User: 'login',
    Group: 'name',
    Grant: 'name',
    AllocationUsage: 'allocation_usages'
}


class MongoStorage(object):
    def __init__(self):
        pass

    def get_db(self):
        mc = MongoClient('mongodb://localhost/hpcbursar')
        return mc['hpcbursar']

    def store_template(self, model_type, instance):
        db = self.get_db()

        serializer = MODEL_TYPE_TO_SERIALIZER[model_type]
        data = serializer(instance).data
        name_field = MODEL_TYPE_TO_NAMEFIELD[model_type]
        name = getattr(instance, name_field)
        db[MODEL_TYPE_TO_COLLECTION[model_type]].find_one_and_replace({name_field: name}, data, upsert=True)

    def find_by_filter_template(self, model_type, query):
        db = self.get_db()
        documents = list(db[MODEL_TYPE_TO_COLLECTION[model_type]].find(query))
        if not documents:
            return documents
        serializer = MODEL_TYPE_TO_SERIALIZER[model_type](data=documents, many=True)
        serializer.is_valid()
        return serializer.save()

    def find_one_by_name_template(self, model_type, name):
        db = self.get_db()

        name_field = MODEL_TYPE_TO_NAMEFIELD[model_type]
        document = db[MODEL_TYPE_TO_COLLECTION[model_type]].find_one({name_field: name})
        if not document:
            return document
        serializer = MODEL_TYPE_TO_SERIALIZER[model_type](data=document)
        serializer.is_valid()
        return serializer.save()

    def find_all_template(self, model_type):
        db = self.get_db()

        documents = list(db[MODEL_TYPE_TO_COLLECTION[model_type]].find({}))
        if not documents:
            return documents
        serializer = MODEL_TYPE_TO_SERIALIZER[model_type](data=documents, many=True)
        serializer.is_valid()
        return serializer.save()

    # stores
    def store_user(self, user):
        self.store_template(User, user)

    def store_group(self, group):
        self.store_template(Group, group)

    def store_grant(self, grant):
        self.store_template(Grant, grant)

    def store_allocation_usage(self, allocation_usage):
        self.store_template(AllocationUsage, allocation_usage)

    # stores many
    # TODO: implement as bulk operation
    def store_users(self, users):
        for user in users:
            self.store_user(user)

    def store_groups(self, groups):
        for group in groups:
            self.store_group(group)

    def store_grants(self, grants):
        for grant in grants:
            self.store_grant(grant)

    def store_allocation_usages(self, allocation_usages):
        for allocation in allocation_usages:
            self.store_allocation_usage(allocation)

    # finds single
    def find_user_by_login(self, login):
        return self.find_one_by_name_template(User, login)

    def find_group_by_name(self, name):
        return self.find_one_by_name_template(Group, name)

    def find_grant_by_name(self, name):
        return self.find_one_by_name_template(Grant, name)

    # finds all
    def find_all_users(self):
        return self.find_all_template(User)

    def find_all_groups(self):
        return self.find_all_template(Group)

    def find_all_grants(self):
        return self.find_all_template(Grant)

    # specific finds
    def find_groups_by_member(self, member):
        return self.find_by_filter_template(Group, {'$or': [
            {'leaders': member},
            {'members': member}
        ]})

    def find_grants_by_group(self, group):
        return self.find_by_filter_template(Grant, {'group': group})

    def find_allocation_usages_by_name(self, name):
        return self.find_by_filter_template(AllocationUsage, {"name": name})

    def find_allocations_by_group(self, group):
        grants = self.find_grants_by_group(group)
        allocations = []
        for g in grants:
            allocations.append(g.allocations)
        return allocations

    def update_usage_in_allocation_usages(self, allocation_name, data):
        db = self.get_db()
        allocations = self.find_allocation_usages_by_name(allocation_name)
        if not allocations:
            raise Exception("Wrong name")
        for alloc in allocation_name:
            usage = alloc["usage"]
            usage.append(data)
            db["allocation_usages"].update_one({"name": allocation_name}, {"$set": {"usage": usage}})
        serializer = MODEL_TYPE_TO_SERIALIZER[AllocationUsage](data=allocations, many=True)
        serializer.is_valid()
        return serializer.save()

    def remove_usage_in_allocation_usages(self, allocation_name, start_date, end_date):
        db = self.get_db()
        allocations = self.find_allocation_usages_by_name(allocation_name)
        if not allocations:
            raise Exception("Wrong name")
        for alloc in allocations:
            usage = alloc["usage"]
            for u in usage:
                if u["start"] > start_date and u["end"] < end_date:
                    usage.remove(u)
            db["allocation_usages"].update_one({"name": allocation_name}, {"$set": {"usage": usage}})
        serializer = MODEL_TYPE_TO_SERIALIZER[AllocationUsage](data=allocations, many=True)
        serializer.is_valid()
        return serializer.save()
