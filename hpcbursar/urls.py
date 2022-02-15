from django.urls import path
from grantstorage.service.user.user_grant_info_view import UserGrantInfoView

urlpatterns = [
    path('api/v1/user/user_grants_info/<login>', UserGrantInfoView.as_view()),
]
