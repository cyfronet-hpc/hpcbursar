from django.core.management.base import BaseCommand, CommandError
from grantstorage.integrations.portalclient import PortalClient
from django.conf import settings
import json
from grantstorage.localmodels.user import User, UserSerializer
from grantstorage.localmodels.group import Group, GroupSerializer
from grantstorage.localmodels.grant import Grant, Allocation, GrantSerializer
from grantstorage.storage.mongo.mongostorage import MongoStorage
import datetime


class Command(BaseCommand):
    help = 'Download grants, groups, users information from portal'

    def setup(self):
        self.pc = PortalClient(
            settings.PLGRID_PORTAL_URL,
            settings.PLGRID_SITE_NAME,
            settings.GRID_KEY_LOCATION,
            settings.GRID_CERTIFICATE_LOCATION
        )

    def convert_recources_to_local(self, resource_type, portal_parameters):
        resource_mapping = {"CPU": {
            "CPUNonGuaranteedComputingTime": "hours",
            "CPUMaxJobWalltime": "timelimit"
        }, "GPU": {
            "GPUNonGuaranteedComputingTime": "hours",
            "GPUMaxTime": "timelimit"
        }, "Storage": {
            "POSIXNonGuaranteedStorage": "capacity",
        }}

        parameters = {}

        for r, v in portal_parameters.items():
            if r in resource_mapping[resource_type]:
                parameters[resource_mapping[resource_type][r]] = v
        return parameters

    def convert_allocation_to_localmodel(self, portal_allocations):

        allocations = []
        for portal_allocation in portal_allocations:
            name = portal_allocation['grantName']
            resource = portal_allocation['resource']
            portal_parameters = portal_allocation['resources']
            parameters = self.convert_recources_to_local(resource, portal_parameters)
            allocation = Allocation(name=name, resource=resource, parameters=parameters)
            allocations += [allocation]
        return allocations

    def convert_grants_to_localmodel(self, portal_grants):
        grants = []
        for portal_grant in portal_grants:
            name = portal_grant['name']
            group = portal_grant['team']
            status = portal_grant['state']
            start = datetime.datetime.fromtimestamp(int(portal_grant['start']) / 1000).date()
            end = datetime.datetime.fromtimestamp(int(portal_grant['end'] / 1000)).date()
            allocations = self.convert_allocation_to_localmodel(portal_grant['olaList'])
            grant = Grant(name=name, group=group, status=status, start=start, end=end, allocations=allocations)
            grants += [grant]
        return grants

    def convert_users_to_localmodels(self, portal_users):
        users = []
        for portal_user in portal_users:
            login = portal_user['login']
            status = portal_user['status']
            user = User(login=login, status=status)
            users += [user]
        return users

    def convert_groups_to_localmodels(self, portal_groups):
        groups = []
        for portal_group in portal_groups:
            name = portal_group['teamId']
            status = portal_group['status']
            members = portal_group['teamMembers']
            leaders = portal_group['teamLeaders']
            group = Group(name=name, status=status, members=members, leaders=leaders)
            groups += [group]
        return groups

    def handle(self, *args, **options):
        self.setup()

        portal_grants = self.pc.download_grants()
        portal_groups = self.pc.download_groups()
        portal_users = self.pc.download_users()

        grants = self.convert_grants_to_localmodel(portal_grants)
        groups = self.convert_groups_to_localmodels(portal_groups)
        users = self.convert_users_to_localmodels(portal_users)

        print('done downloading')
        ms = MongoStorage()
        ms.store_users(users)
        ms.store_groups(groups)
        ms.store_grants(grants)
        print('done stores')
