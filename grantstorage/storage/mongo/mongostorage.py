from pymongo import MongoClient
from grantstorage.localmodels.user import User, UserSerializer
from grantstorage.localmodels.group import Group, GroupSerializer
from grantstorage.localmodels.grant import Grant, Allocation, GrantSerializer

MODEL_TYPE_TO_COLLECTION = {
    User: 'user',
    Group: 'group',
    Grant: 'grant'
}

MODEL_TYPE_TO_SERIALIZER = {
    User: UserSerializer,
    Group: GroupSerializer,
    Grant: GrantSerializer
}

MODEL_TYPE_TO_NAMEFIELD = {
    User: 'login',
    Group: 'name',
    Grant: 'name'
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

    def find_template(self, model_type, name):
        db = self.get_db()

        name_field = MODEL_TYPE_TO_NAMEFIELD[model_type]
        document = db[MODEL_TYPE_TO_COLLECTION[model_type]].find_one({name_field: name})
        serializer = MODEL_TYPE_TO_SERIALIZER[model_type](data=document)
        serializer.is_valid()
        return serializer.save()

    def find_all_template(self, model_type):
        db = self.get_db()

        name_field = MODEL_TYPE_TO_NAMEFIELD[model_type]
        document = list(db[MODEL_TYPE_TO_COLLECTION[model_type]].find({}))
        serializer = MODEL_TYPE_TO_SERIALIZER[model_type](data=document, many=True)
        serializer.is_valid()
        return serializer.save()

    # stores
    def store_user(self, user):
        self.store_template(User, user)

    def store_group(self, group):
        self.store_template(Group, group)

    def store_grant(self, grant):
        self.store_template(Grant, grant)

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

    # finds single
    def find_user(self, login):
        return self.find_template(User, login)

    def find_group(self, name):
        return self.find_template(Group, name)

    def find_grant(self, name):
        return self.find_template(Grant, name)

    # finds all
    def find_all_users(self):
        return self.find_all_template(User)

    def find_all_groups(self):
        return self.find_all_template(Group)

    def find_all_grants(self):
        return self.find_all_template(Grant)
