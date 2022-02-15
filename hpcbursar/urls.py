from django.urls import path
from grantstorage.service.v1.user.views.user_grant_info_view import UserGrantInfoView
from grantstorage.service.v1.admin.views.admin_grant_group_info import AdminGrantGroupInfoView

urlpatterns = [
    #user
    path('api/v1/user/grants_info/<login>', UserGrantInfoView.as_view()),
    #admi
    path('api/v1/admin/grants_group_info/', AdminGrantGroupInfoView.as_view()),
]
