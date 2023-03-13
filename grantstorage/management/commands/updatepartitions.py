# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.core.management.base import BaseCommand, CommandError
from grantstorage.integration.scontrolclient import ScontrolClient
from django.conf import settings
from grantstorage.storage.mongo.mongostorage import MongoStorage
import datetime


class Command(BaseCommand):
    help = 'Generate Slurm sacct configuration based on grant/group/user data.'

    def setup(self):
        self.ms = MongoStorage()
        self.sc = ScontrolClient()

    def is_grant_active(self, grant):
        end = grant.end + datetime.timedelta(days=1)
        if (end >= datetime.datetime.now().date() and grant.start <= datetime.datetime.now().date() and 'accepted' in grant.status) or 'active' in grant.status:
            return True
        else:
            return False

    def handle(self, *args, **options):
        self.setup()

        grants = self.ms.find_all_grants()
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)

        partition_mapping = settings.SLURM_PARTITION_MAPPING
        partition_account = {}

        for grant in grants:
            if grant.is_active:
                for allocation in grant.allocations:
                    for cond, partitions in partition_mapping.items():
                        if cond(allocation):
                            for partition in partitions:
                                if partition in partition_account.keys():
                                    partition_account[partition] += [allocation.name]
                                else:
                                    partition_account[partition] = [allocation.name]

        # print(json.dumps(partition_account, indent=2))
        for partition, accounts in partition_account.items():
            if not accounts:
                pass
            self.sc.set_partition_accounts(partition, accounts)
