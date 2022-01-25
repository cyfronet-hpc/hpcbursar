from django.urls import include, path
from rest_framework import routers
from grantstorage.views import UserViewSet, GrantViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'grant', GrantViewSet)
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]