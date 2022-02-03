from django.urls import path
from grantstorage.views import UserServicesView

urlpatterns = [
    path('api/v1/user/user_grants_info/<login>', UserServicesView.as_view()),
]
