# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

import json

import requests
import jwt
import datetime

# API_V1_URL_BASE = 'api/v1.0/'
API_V2_URL_BASE = 'api/sites/'


class PortalException(Exception):
    pass


class PortalClient(object):
    def __init__(self, portal_v2_url, site_names, ecprivkey_path):
        self.user_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/users'
        self.group_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/groups'
        self.grant_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/grants'
        self.allocation_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/allocations'

        self.site_names = site_names
        self.ecprivkey_path = ecprivkey_path

    def portal_v2_request(self, url, token):
        print("URL:", url)
        headers = {'Authorization': 'Bearer %s' % token}
        response = requests.get(url, headers=headers)
        return response.json()

    def download_grants(self):
        with open(self.ecprivkey_path, 'rb') as f:
            private_key = f.read()

        results = []
        for site in self.site_names:
            date_future = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%s')
            encoded = jwt.encode({'name': site, 'exp': date_future}, private_key, algorithm='ES512')
            results += [self.portal_v2_request(self.grant_url % site, encoded)['grants']]
        return results

    def download_allocations(self):
        with open(self.ecprivkey_path, 'rb') as f:
            private_key = f.read()

        results = []
        for site in self.site_names:
            date_future = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%s')
            encoded = jwt.encode({'name': site, 'exp': date_future}, private_key, algorithm='ES512')
            results += [self.portal_v2_request(self.allocation_url % site, encoded)['allocations']]
        return results

    def download_groups(self):
        with open(self.ecprivkey_path, 'rb') as f:
            private_key = f.read()

        results = []
        for site in self.site_names:
            date_future = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%s')
            encoded = jwt.encode({'name': site, 'exp': date_future}, private_key, algorithm='ES512')
            results += [self.portal_v2_request(self.group_url % site, encoded)['groups']]
        return results

    def download_users(self):
        with open(self.ecprivkey_path, 'rb') as f:
            private_key = f.read()

        results = []
        for site in self.site_names:
            date_future = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime('%s')
            encoded = jwt.encode({'name': site, 'exp': date_future}, private_key, algorithm='ES512')
            results += [self.portal_v2_request(self.user_url % site, encoded)['users']]
        return results


# if __name__ == '__main__':
#     pc = PortalClient(
#         'https://portal.pre.plgrid.pl/',
#         ['CYFRONET-ARES', 'CYFRONET-HPC-STORAGE'],
#         '/home/yaq/.globus/ecdsa-p521-private.pem'
#     )

    # print(json.dumps(pc.download_allocations()))
    # print(json.dumps(pc.download_grants()))
    # print(pc.download_users())
