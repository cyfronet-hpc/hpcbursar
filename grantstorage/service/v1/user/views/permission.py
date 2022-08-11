# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

import pymunge
from rest_framework.permissions import BasePermission


class UserGrantInfoMungePermission(BasePermission):
    def has_permission(self, request, view):
        if "x-auth-hpcbursar" in request.headers:
            encoded_x_hb_auth_token = str.encode(request.headers["x-auth-hpcbursar"])
            with pymunge.MungeContext() as ctx:
                payload, uid, gid = ctx.decode(encoded_x_hb_auth_token)
                decoded_payload = payload.decode('utf-8')
                username, service_request = decoded_payload.split(":")
                request_username = request.build_absolute_uri().split('/')[-1]
                if username == request_username:
                    return True
        print("No permission")
        return False
