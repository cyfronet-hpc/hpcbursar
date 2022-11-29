from django.core.management.base import BaseCommand
from grantstorage.integration.portalclient.v2 import PortalClient
from django.conf import settings
from grantstorage.localmodels.user import User
from grantstorage.localmodels.group import Group
from grantstorage.localmodels.grant import Grant, Allocation
from grantstorage.storage.mongo.mongostorage import MongoStorage
import datetime

DATE_FMT = '%Y-%m-%d'


class Command(BaseCommand):
    help = 'Download grants, groups, users information from portal'

    def setup(self):
        self.pc = PortalClient(
            settings.PLGRID_PORTAL_V1_URL,
            settings.PLGRID_PORTAL_V2_URL,
            settings.PLGRID_SITE_NAMES,
            settings.GRID_KEY_LOCATION,
            settings.GRID_CERTIFICATE_LOCATION,
            settings.EC_PRIVKEY_LOCATION,
        )

    def convert_recources_to_local(self, resource_type, portal_parameters):
        resource_mapping = {"cpu": {
            "time": "hours",
            "max-execution-time": "timelimit"
        }, "gpu": {
            "time": "hours",
        }, "storage": {
            "capacity": "capacity",
        }
        }

        parameters = {}

        for r, v in portal_parameters.items():
            if r in resource_mapping[resource_type]:
                parameters[resource_mapping[resource_type][r]] = v
        return parameters

    def convert_grants_to_localmodel(self, portal_grant_lists, portal_allocation_lists):

        grant_allocations = {}
        for portal_allocation_list in portal_allocation_lists:
            for portal_allocation in portal_allocation_list:
                # name = portal_allocation['grantName'] + '-' + portal_allocation['resource'].lower()
                name = portal_allocation['name']
                resource = portal_allocation['resource']
                portal_parameters = portal_allocation['parameterValues']
                if resource.startswith('storage'):
                    resource = 'storage'
                parameters = self.convert_recources_to_local(resource, portal_parameters)
                grant_name = portal_allocation['grantName']
                allocation = Allocation(name=name, resource=resource, parameters=parameters)
                if grant_name not in grant_allocations.keys():
                    grant_allocations[grant_name] = [allocation]
                else:
                    grant_allocations[grant_name] += [allocation]

        grants = {}
        for portal_grants in portal_grant_lists:
            for portal_grant in portal_grants:
                # try:
                name = portal_grant['name']
                group = portal_grant['team']
                status = portal_grant['status']
                start = datetime.datetime.strptime(portal_grant['start'], DATE_FMT).date()
                end = datetime.datetime.strptime(portal_grant['end'], DATE_FMT).date()
                grant = Grant(name=name, group=group, status=status, start=start, end=end,
                              allocations=grant_allocations.get(name, []))
                grants[name] = grant
                # except:
                #     pass
        return grants.values()

    def convert_users_to_localmodels(self, portal_user_list):
        users = {}
        for portal_users in portal_user_list:
            for portal_user in portal_users:
                login = portal_user['login']
                status = portal_user['status']
                user = User(login=login, status=status)
                users[login] = user
        return users.values()

    def convert_groups_to_localmodels(self, portal_group_list):
        groups = {}
        for portal_groups in portal_group_list:
            for portal_group in portal_groups:
                name = portal_group['teamId']
                status = portal_group['status']
                members = portal_group['teamMembers']
                leaders = portal_group['teamLeaders']
                group = Group(name=name, status=status, members=members, leaders=leaders)
                groups[name] = group
        return groups.values()

    def handle(self, *args, **options):
        self.setup()

        portal_grants = self.pc.download_grants()
        portal_allocations = self.pc.download_allocations()
        portal_groups = self.pc.download_groups()
        portal_users = self.pc.download_users()

        grants = self.convert_grants_to_localmodel(portal_grants, portal_allocations)
        groups = self.convert_groups_to_localmodels(portal_groups)
        users = self.convert_users_to_localmodels(portal_users)

        print('done downloading: grants: ' + str(len(grants)) + ', groups: ' + str(len(groups)) + ', users: ' + str(len(users)))
        ms = MongoStorage()
        ms.store_users(users)
        ms.store_groups(groups)
        ms.store_grants(grants)
        print('done stores')
