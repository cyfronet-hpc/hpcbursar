# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.urls import path
from grantstorage.service.v1.user.views.user_grant_info_view import UserGrantInfoView
from grantstorage.service.v1.admin.views.admin_grant_group_info import AdminGrantGroupInfoView

urlpatterns = [
    # user
    path('api/v1/user/grants_info/<login>', UserGrantInfoView.as_view(), name="grants_info"),
    # admin
    path('api/v1/admin/grants_group_info/', AdminGrantGroupInfoView.as_view(), name="admin"),
    # allocation usage
    # path('api/v1/allocation_usage', UserAllocationInfoView.as_view(), name="allocations_info")
]
