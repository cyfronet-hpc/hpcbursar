# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.core.management.base import BaseCommand
from grantstorage.integration.sacctmgrclient import SacctmgrClient
from django.conf import settings
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
        if (
                end >= datetime.datetime.now().date() >= grant.start and 'accepted' in grant.status) or 'active' in grant.status:
            return True
        else:
            return False

    def is_allocation_active(self, allocation):
        end = allocation.end + datetime.timedelta(days=1)
        if (
                end >= datetime.datetime.now().date() >= allocation.start and 'accepted' in allocation.status) or 'active' in allocation.status:
            return True
        else:
            return False

    def find_user_managed_accounts(self, users, group_dict, grants):
        user_grants_dict = {}
        for user in users:
            # make sure all users are in the dict!
            user_grants_dict[user] = []

        for grant in grants:
            group = group_dict[grant.group]
            for user in group.get_all_members():
                if user not in user_grants_dict.keys():
                    user_grants_dict[user] = [grant]
                else:
                    user_grants_dict[user] += [grant]

        user_account_dict = {}
        for user, grants in user_grants_dict.items():
            user_account_dict[user] = []

            user_allocations = []
            # grants.sort(key=lambda g: g.start)
            for grant in grants:
                for allocation in grant.allocations:
                    if allocation.resource in settings.SLURM_SUPPORTED_RESOURCES:
                        if allocation.is_active:
                            user_allocations += [allocation]

            user_allocations.sort(key=lambda a: a.start)
            user_account_dict[user] = list(map(lambda a: a.name, user_allocations))

        return user_account_dict

    def filter_group_users(self, group, user_logins):
        new_members = []
        new_leaders = []
        for user in group.members:
            if user in user_logins:
                new_members += [user]
        for user in group.leaders:
            if user in user_logins:
                new_leaders += [user]

        group.members = new_members
        group.leaders = new_leaders

        return group

    def find_user_unmanaged_accounts(self, users, grants, slurm_assoc):
        managed_accounts = []
        user_unmanaged = {}
        for user in users:
            user_unmanaged[user] = []
        for grant in grants:
            for allocation in grant.allocations:
                managed_accounts += [allocation.name]

        for user in users:
            for slurm_account, params in slurm_assoc.items():
                if user in params['users'].keys() and slurm_account not in managed_accounts:
                    if user in user_unmanaged.keys():
                        user_unmanaged[user] += [slurm_account]
                    else:
                        user_unmanaged[user] = [slurm_account]

        return user_unmanaged

    # modify sacctmgr
    def verify_default_accounts(self, users, slurm_user_da, user_managed_accounts, user_unmanaged_accounts):
        for user in users:
            if user in slurm_user_da.keys():
                slurm_default_account = slurm_user_da[user]
                managed_accounts = user_managed_accounts[user]
                unmanaged_accounts = user_unmanaged_accounts[user]
                if slurm_default_account in managed_accounts or slurm_default_account in unmanaged_accounts:
                    continue
                else:
                    if managed_accounts:
                        self.sc.update_user_default_account(user, managed_accounts[0])
                    elif unmanaged_accounts:
                        self.sc.update_user_default_account(user, unmanaged_accounts[0])
                    else:
                        self.sc.remove_user(user)

    def add_slurm_account(self, allocation, group):
        fs = self.calculate_fairshare(allocation.start, allocation.end, allocation.parameters['hours'])
        self.sc.add_account(allocation.name, fs)
        for user in group.get_all_members():
            self.sc.add_user_account(user, allocation.name)

    def sync_slurm_account(self, allocation, group, slurm_account, managed_users):
        if not allocation.is_active:
            for user in slurm_account['users'].keys():
                self.sc.remove_user_account(user, allocation.name)
            self.sc.remove_account(allocation.name)
            return

        fs = self.calculate_fairshare(allocation.start, allocation.end, allocation.parameters['hours'])
        if slurm_account['fairshare'] != fs:
            self.sc.update_account_fairshare(allocation.name, fs)
        if slurm_account['maxsubmit'] == 0:
            self.sc.update_account_maxsubmit(allocation.name, -1)

        for user in group.get_all_members():
            if user not in slurm_account['users'].keys():
                self.sc.add_user_account(user, allocation.name)
            else:
                if slurm_account['users'][user]['maxsubmit'] == 0:
                    # TODO are we sure that the maxsubmit can be reversed?
                    self.sc.update_user_account_maxsubmit(user, allocation.name, -1)

        for slurm_user in slurm_account['users'].keys():
            if slurm_user not in group.get_all_members() and slurm_user in managed_users:
                self.sc.remove_user_account(slurm_user, allocation.name)

    def handle(self, *args, **options):
        self.setup()

        users = self.ms.find_all_users()
        groups = self.ms.find_all_groups()
        # grants = list(filter(lambda grant: grant.name == 'plgplgrid', self.ms.find_all_grants()))
        grants = self.ms.find_all_grants()
        users = list(filter(lambda user: user.status.lower() == 'active', users))
        user_dict = {}
        group_dict = {}
        for user in users:
            user_dict[user.login] = user
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)
            for allocation in grant.allocations:
                allocation.is_active = self.is_allocation_active(allocation)
        for group in groups:
            self.filter_group_users(group, user_dict.keys())
            group_dict[group.name] = group

        slurm_assoc = self.sc.get_assoc_dict()
        slurm_user_da_dict = self.sc.get_user_default_account_dict()

        print('adding grants')
        for grant in grants:
            for allocation in grant.allocations:
                if allocation.resource in settings.SLURM_SUPPORTED_RESOURCES:
                    if allocation.is_active:
                        if allocation.name not in slurm_assoc.keys():
                            self.add_slurm_account(allocation, group_dict[grant.group])

        print('find managed user_accounts')
        user_managed_accounts = self.find_user_managed_accounts(user_dict.keys(), group_dict, grants)

        print('find unmanaged user_accounts')
        user_unmanaged_accounts = self.find_user_unmanaged_accounts(user_dict.keys(), grants, slurm_assoc)

        print('verify_default_accounts')
        # move removing users to post 'sync_slurm_accounts'
        self.verify_default_accounts(user_dict.keys(), slurm_user_da_dict, user_managed_accounts,
                                     user_unmanaged_accounts)

        print('sync_slurm_accounts')
        for grant in grants:
            for allocation in grant.allocations:
                if allocation.resource in settings.SLURM_SUPPORTED_RESOURCES:
                    if allocation.name in slurm_assoc.keys():
                        self.sync_slurm_account(allocation, group_dict[grant.group], slurm_assoc[allocation.name],
                                                user_dict.keys())
