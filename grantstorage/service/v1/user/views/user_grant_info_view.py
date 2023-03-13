# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from grantstorage.service.v1.user.controller.userservice import UserServicesController
from grantstorage.service.v1.user.views.user_grant_info import UserGrantInfoResponse, UserGrantInfoSerializer
from grantstorage.service.v1.user.views.user_grant_info_permission import UserGrantInfoMungePermission


class UserGrantInfoView(APIView):
    permission_classes = [UserGrantInfoMungePermission]

    def get(self, request, login):
        user_service_controller = UserServicesController()
        grants_dict = user_service_controller.user_grant_info(login)
        # allocation_usages_dict = user_service_controller.user_allocation_info(login)
        response = []
        for grant, attrs in grants_dict.items():
            group, allocation_usages = attrs
            user_info_model = UserGrantInfoResponse(grant, group, allocation_usages)
            user_info_serializer = UserGrantInfoSerializer(user_info_model)
            response.append(user_info_serializer.data)
        return Response(response)
