import requests

API_URL_BASE = 'api/v1.0/'


class PortalException(Exception):
    pass


class PortalClient(object):
    def __init__(self, portal_url, site_name, key_path, cert_path):
        self.grant_url = portal_url + API_URL_BASE + 'grant?site=' + site_name
        self.group_url = portal_url + API_URL_BASE + 'group?site=' + site_name
        self.user_url = portal_url + API_URL_BASE + 'user?site=' + site_name

        self.key_path = key_path
        self.cert_path = cert_path

    def portal_request(self, url):
        response = requests.get(url, cert=(self.cert_path, self.key_path))
        return response.json()

    def download_grants(self):
        return self.portal_request(self.grant_url)

    def download_groups(self):
        return self.portal_request(self.group_url)

    def download_users(self):
        return self.portal_request(self.user_url)
