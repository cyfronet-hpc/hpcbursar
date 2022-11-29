import json

import requests
import jwt
import datetime

API_V1_URL_BASE = 'api/v1.0/'
API_V2_URL_BASE = 'api/sites/'


class PortalException(Exception):
    pass


class PortalClient(object):
    def __init__(self, portal_v1_url, portal_v2_url, site_names, key_path, cert_path, ecprivkey_path):
        self.group_url = portal_v1_url + API_V1_URL_BASE + 'group?site='
        self.user_url = portal_v1_url + API_V1_URL_BASE + 'user?site='

        self.allocation_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/allocations'
        self.grant_url = portal_v2_url + API_V2_URL_BASE + '%s' + '/grants'

        self.site_names = site_names
        self.key_path = key_path
        self.cert_path = cert_path
        self.ecprivkey_path = ecprivkey_path

    def portal_v1_request(self, url):
        response = requests.get(url, cert=(self.cert_path, self.key_path))
        return response.json()

    def portal_v2_request(self, url, token):
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
        results = []
        for site in self.site_names:
            results += [self.portal_v1_request(self.group_url + site)]
        return results

    def download_users(self):
        results = []
        for site in self.site_names:
            results += [self.portal_v1_request(self.user_url + site)]
        return results


# if __name__ == '__main__':
#     pc = PortalClient(
#         'https://portal.plgrid.pl/',
#         'https://grants.pre.plgrid.pl/',
#         ['CYFRONET-ARES', 'CYFRONET-HPC-STORAGE'],
#         '/home/yaq/.globus/userkey-insec.pem',
#         '/home/yaq/.globus/usercert.pem',
#         '/home/yaq/.globus/ecdsa-p521-private.pem'
#     )

    # print(json.dumps(pc.download_allocations()))
    # print(json.dumps(pc.download_grants()))
    # print(pc.download_users()[1])
