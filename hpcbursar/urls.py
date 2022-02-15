from django.urls import path
from grantstorage.service.v1.user import UserGrantInfoView

urlpatterns = [
    path('api/v1/user/user_grants_info/<login>', UserGrantInfoView.as_view()),
    path('api/v1/user/user_grants_info/<login>', UserGrantInfoView.as_view()),
]
