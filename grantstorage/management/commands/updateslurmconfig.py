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
        if end > datetime.datetime.now().date() and grant.start < datetime.datetime.now().date() and 'binding' in grant.status:
            return True
        else:
            return False

    def find_default_accounts(self, users, group_dict, grants):
        user_grants_dict = {}
        for user in users:
            user_grants_dict[user.login] = []

        for grant in grants:
            if not grant.is_active:
                continue
            group = group_dict[grant.group]
            for user in set(group.members + group.leaders):
                if user not in user_grants_dict.keys():
                    user_grants_dict[user] = [grant]
                else:
                    user_grants_dict[user] += [grant]

        user_grant_dict = {}
        for user, grants in user_grants_dict.items():
            default_account = None
            if len(grants) > 0:
                grants.sort(key=lambda g: g.start)
                default_grant = grants[0]
                allocations_dict = {}
                for allocation in default_grant.allocations:
                    allocations_dict[allocation.resource] = allocation
                if "CPU" in allocations_dict.keys():
                    default_account = allocations_dict["CPU"].name
                elif "GPU" in allocations_dict.keys():
                    default_account = allocations_dict["GPU"].name

            user_grant_dict[user] = default_account

        return user_grant_dict

    # modify sacctmgr
    def verify_default_accounts(self, user_da, slurm_user_da):
        for user, default_account in user_da.items():
            if user in slurm_user_da.keys():
                if not default_account:
                    self.sc.remove_user(user)
                    continue
                if default_account != slurm_user_da[user]:
                    self.sc.update_user_default_account(user, default_account)

    def set_default_accounts(self, user_list, user_da):
        pass

    def add_slurm_account(self, grant, allocation, group):
        print("adding", allocation)
        fs = self.calculate_fairshare(grant.start, grant.end, allocation.parameters['hours'])
        self.sc.add_account(allocation.name, fs)
        for user in set(group.members + group.leaders):
            self.sc.add_user_account(user, allocation.name)

    def sync_slurm_account(self, grant, allocation, group, slurm_account):
        if not grant.is_active:
            for user in slurm_account['users'].keys():
                self.sc.remove_user_account(user, allocation.name)
            self.sc.remove_account(allocation.name)
            return

        fs = self.calculate_fairshare(grant.start, grant.end, allocation.parameters['hours'])
        if slurm_account['fairshare'] != fs:
            self.sc.update_account_fairshare(allocation.name, fs)
        if slurm_account['maxsubmit'] == 0:
            self.sc.update_user_maxsubmit(-1)

        for user in set(group.members + group.leaders):
            if user not in slurm_account['users'].keys():
                self.sc.add_user_account(user, allocation.name)
            else:
                if slurm_account['users'][user]['maxsubmit'] == 0:
                    self.sc.update_user_account_maxsubmit(user, allocation.name, -1)

        for slurm_user in slurm_account['users'].keys():
            if slurm_user not in set(group.members + group.leaders):
                self.sc.remove_user_account(slurm_user, allocation.name)

    def handle(self, *args, **options):
        self.setup()

        grants = self.ms.find_all_grants()
        groups = self.ms.find_all_groups()
        group_dict = {}
        users = self.ms.find_all_users()
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)
        for group in groups:
            group_dict[group.name] = group
        user_da_dict = self.find_default_accounts(users, group_dict, grants)

        slurm_assoc = self.sc.get_assoc_dict()
        slurm_user_da_dict = self.sc.get_user_defaccount_dict()

        for grant in grants:
            for allocation in grant.allocations:
                if allocation.resource in ["CPU", "GPU"]:
                    if allocation.name not in slurm_assoc.keys():
                        self.add_slurm_account(grant, allocation, group_dict[grant.group])

        self.verify_default_accounts(user_da_dict, slurm_user_da_dict)

        for grant in grants:
            for allocation in grant.allocations:
                if allocation.resource in ["CPU", "GPU"]:
                    if allocation.name in slurm_assoc.keys():
                        self.sync_slurm_account(grant, allocation, group_dict[grant.name], slurm_assoc[allocation.name])

        # set proper default account for ppl added with new accounts
        new_user_da_dict = {}
        for user in user_da_dict.keys():
            if user not in slurm_user_da_dict.keys():
                new_user_da_dict[user] = user_da_dict[user]
        # get information about current default accounts
        slurm_user_da_dict = self.sc.get_user_defaccount_dict()
        self.verify_default_accounts(new_user_da_dict, slurm_user_da_dict)

        # new new idea
        # 1. add new accounts
        # 2. update def accounts for existing ppl, remove ppl without def acct
        # 3. synchronize old accounts
        #     if deleting account remove all
        #     add new ppl
        #     remove old ppl
        #     check maxsubmit for existing ppl
        #     check fairshare, correct if needed
        # 4. check default grant for new ppl

        # new idea
        # 1. update default accounts, remove ppl without them
        # 2. update accounts one by one
        # 3. fix def account for ppl failed at step 1
        # 4. set default account for new ppl

        # old idea
        # add stuff
        # update def accounts for all ppl
        # delete ppl without default account
        # check/update fairshare (for previously existing grants)
        # check/update maxsubmit (for prebiously existing grants)
        # remove stuff
        # if impossible set maxsubmit = 0
