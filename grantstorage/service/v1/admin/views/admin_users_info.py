# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from grantstorage.service.v1.admin.controller.adminservice import AdminServicesController
from .admin_permission import AdminPermission


class AdminAffiliationInfo(object):
    def __init__(self, affiliation):
        self.type = affiliation.type
        self.units = affiliation.units
        self.status = affiliation.status
        self.end = affiliation.end


class AdminAffiliationInfoSerializer(serializers.Serializer):
    type = serializers.CharField()
    units = serializers.ListField(child=serializers.CharField())
    status = serializers.CharField()
    end = serializers.DateField()


class AdminUserInfo(object):
    def __init__(self, user):
        self.login = user.login
        self.email = user.email
        self.status = user.status
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.opi = user.opi
        self.affiliations = [AdminAffiliationInfo(affiliation) for affiliation in user.affiliations]


class AdminUserInfoSerializer(serializers.Serializer):
    login = serializers.CharField()
    email = serializers.CharField()
    status = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    opi = serializers.CharField(allow_blank=True)
    affiliations = AdminAffiliationInfoSerializer(many=True)


class AdminUsersInfo(APIView):
    permission_classes = [AdminPermission]

    def get(self, login):
        admin_service_controller = AdminServicesController()
        user = admin_service_controller.user_info(login)
        user_info = AdminUserInfo(user)
        response = AdminUserInfoSerializer(user_info)
        return Response(response.data)
