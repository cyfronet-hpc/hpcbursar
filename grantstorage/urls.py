# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.urls import path
from grantstorage.service.v1.user.views.user_grant_info_view import UserGrantInfoView
from grantstorage.service.v1.admin.views.admin_grant_group_info import AdminGrantGroupInfoView
from grantstorage.service.v1.admin.views.admin_grants_info import AdminGrantsInfo
from grantstorage.service.v1.admin.views.admin_users_info import AdminUsersInfo
from grantstorage.service.v1.admin.views.admin_groups_info import AdminGroupsInfo
from grantstorage.service.v1.admin.views.admin_allocations_info import AdminAllocationsInfo

urlpatterns = [
    # user
    path('user/grants_info/<login>/', UserGrantInfoView.as_view(), name="grants_info"),
    # admin
    path('admin/grants_group_info/', AdminGrantGroupInfoView.as_view(), name="grants_group_info"),
    path('admin/grants/<name>/', AdminGrantsInfo.as_view(), dname="admin_grants"),
    path('admin/users/<login>/', AdminUsersInfo.as_view(), name="admin_users"),
    path('admin/groups/<name>/', AdminGroupsInfo.as_view(), name="admin_groups"),
    path('admin/allocations/<name>/', AdminAllocationsInfo.as_view(), name="admin_allocations"),
]
