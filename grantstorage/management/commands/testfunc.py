from django.core.management.base import BaseCommand, CommandError
import json
from grantstorage.localmodels.user import User, UserSerializer
from grantstorage.localmodels.group import Group, GroupSerializer
from grantstorage.localmodels.grant import Grant, GrantSerializer, Allocation
from rest_framework.renderers import JSONRenderer
from grantstorage.storage.mongo.mongostorage import MongoStorage


class Command(BaseCommand):
    help = 'Test some functionality'

    def handle(self, *args, **options):
        ms = MongoStorage()

        # grants = ms.find_grant_by_group('plgglaoisi')
        # for g in grants:
        #     print(GrantSerializer(g).data)

        print(ms.find_user_by_login('plgpawlik'))