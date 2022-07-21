from django.urls import path
from grantstorage.service.v1.user.views.user_grant_info_view import UserGrantInfoView
from grantstorage.service.v1.admin.views.admin_grant_group_info import AdminGrantGroupInfoView
from grantstorage.service.v1.user.views.user_allocation_info_view import UserAllocationInfoView

urlpatterns = [
    # user
    path('api/v1/user/grants_info/<login>', UserGrantInfoView.as_view(), name="grants_info"),
    # admin
    path('api/v1/admin/grants_group_info/', AdminGrantGroupInfoView.as_view(), name="admin"),
    # allocation usage
    # path('api/v1/allocation_usage', UserAllocationInfoView.as_view(), name="allocations_info")
]
