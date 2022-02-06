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
        self.sc = SlurmClient()

    def handle(self, *args, **options):
        self.setup()

        #get grants, groups, users
        # - check time, check state
        # generate resource - acctount names

        # get accounts, users from slurm
        # add accounts
        # add users

        # get assoc from slurm
        # add missing associations
        # update fairshare





