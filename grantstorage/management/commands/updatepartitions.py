from django.core.management.base import BaseCommand, CommandError
from grantstorage.integration.scontrolclient import ScontrolClient
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
        self.sc = ScontrolClient()

    def is_grant_active(self, grant):
        end = grant.end + datetime.timedelta(days=1)
        if end > datetime.datetime.now().date() and grant.start < datetime.datetime.now().date() and 'binding' in grant.status:
            return True
        else:
            return False

    def handle(self, *args, **options):
        self.setup()

        grants = self.ms.find_all_grants()
        for grant in grants:
            grant.is_active = self.is_grant_active(grant)

        resource_partition_mapping = settings.SLURM_RESOURCE_PARTITION_MAPPING
        partition_account = {}
        for resource in resource_partition_mapping.values():
            partition_account[resource] = []

        for grant in grants:
            if grant.is_active:
                for allocation in grant.allocations:
                    if allocation.resource in settings.SLURM_RESOURCE_PARTITION_MAPPING.items():
                        partition_account[resource_partition_mapping[resource]] += [allocation.name]

        for partition, accounts in partition_account.items():
            if not accounts:
                pass
            self.sc.set_partition_accounts(partition, accounts)
