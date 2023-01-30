# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('grantstorage.urls'), name="admin"),
]
