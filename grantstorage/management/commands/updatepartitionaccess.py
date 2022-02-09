from django.core.management.base import BaseCommand, CommandError
from grantstorage.integration.slurmclient import SacctmgrClient
from django.conf import settings
import json
from grantstorage.localmodels.user import User, UserSerializer
from grantstorage.localmodels.group import Group, GroupSerializer
from grantstorage.localmodels.grant import Grant, Allocation, GrantSerializer
from grantstorage.storage.mongo.mongostorage import MongoStorage
import datetime


class Command(BaseCommand):
    help = 'Generate Slurm partition config based on grant data.'

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctmgrClient()

    def is_grant_active(self, grant):
        end = grant.end + datetime.timedelta(days=1)
        if end > datetime.datetime.now().date() and grant.start < datetime.datetime.now().date() and 'binding' in grant.status:
            return True
        else:
            return False

    def handle(self, *args, **options):
        self.setup()

        users = self.ms.find_all_users()
        groups = self.ms.find_all_groups()
        # grants = list(filter(lambda grant: grant.name == 'plgplgrid', self.ms.find_all_grants()))
        grants = self.ms.find_all_grants()
        users = list(filter(lambda user: user.status == 'ACTIVE', users))
        grant_dict = {}
        user_dict = {}
        group_dict = {}
        for user in users:
            user_dict[user.login] = user
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)
            grant_dict[grant.name] = grant
        for group in groups:
            self.filter_group_users(group, user_dict.keys())
            group_dict[group.name] = group
