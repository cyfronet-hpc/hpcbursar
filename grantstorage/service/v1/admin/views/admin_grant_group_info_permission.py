import pwd
import pymunge
from rest_framework.permissions import BasePermission

from django.conf import settings


class AdminMungePermission(BasePermission):
    def has_permission(self, request, view):
        if "x-auth-hpcbursar" in request.headers:
            encoded_x_hb_auth_token = str.encode(request.headers["x-auth-hpcbursar"])
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(encoded_x_hb_auth_token)
                decoded_payload = payload.decode('utf-8')
                username, service_request = decoded_payload.split(":")
                request_username = request.build_absolute_uri().split('/')[-1]
                uid_username = None
                try:
                    uid_username = pwd.getpwuid(uid)[0]
                except KeyError:
                    print('Unknown uid!')
                if username == settings.SLURM_ADMIN_USER and username == uid_username:
                    return True
        return False
