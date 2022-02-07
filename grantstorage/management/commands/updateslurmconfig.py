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
    help = 'Generate Slurm sacct configuration based on grant/group/user data.'

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctmgrClient()
        self.fairshre_window = datetime.timedelta(days=3)

    def calculate_fairshare(self, start, end_raw, hours):
        end = end_raw + datetime.timedelta(days=1)
        duration = end - start
        fs = hours * 3600 / duration.total_seconds() * self.fairshre_window.total_seconds()
        return int(fs)

    def is_grant_active(self, grant):
        end = grant.end + datetime.timedelta(days=1)
        if end > datetime.datetime.now().date() and grant.start < datetime.datetime.now() and 'binding' in grant.status:
            return True
        else:
            return False

    def find_default_accounts(self, users, groups, grants):
        user_grants_dict = {}
        for user in users:
            user_grants_dict[user.login] = []

        group_dict = {}
        for group in groups:
            group_dict[group.name] = group

        for grant in grants:
            if not grant.is_active:
                continue
            group = group_dict[grant.group]
            for user in set(group.members + group.leaders):
                user_grants_dict += [grant]

        user_grant_dict = {}
        for user, grants in user_grants_dict.items():
            grants.sort(key=lambda g: g.start)
            user_grant_dict[user] = grants[0] if len(grants) > 1 else None

    def handle(self, *args, **options):
        self.setup()

        grants = self.ms.find_all_grants()
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)
        groups = self.ms.find_all_groups()
        users = self.ms.find_all_users()

        # add stuff
        # update def accounts for all ppl
        # delete ppl without default account
        # check/update fairshare (for previously existing grants)
        # check/update maxsubmit (for prebiously existing grants)
        # remove stuff
        # if impossible set maxsubmit = 0
