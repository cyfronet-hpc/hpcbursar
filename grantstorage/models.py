from datetime import datetime

from django.db import models


class OlaList(models.Model):
    createdAt = models.DateTimeField()
    end = models.DateTimeField()
    grantName = models.TextField()
    provider = models.TextField()
    resource = models.TextField()
    resources = models.TextField()
    site = models.TextField()
    start = models.DateTimeField()


class Grant(models.Model):
    description = models.TextField()
    end = models.DateTimeField(default=datetime.now, blank=True)
    name = models.TextField()
    start = models.DateTimeField(default=datetime.now, blank=True)
    state = models.TextField()
    team = models.TextField()
    # ola_list = models.ForeignKey(OlaList, on_delete=models.CASCADE)


class User(models.Model):
    pass


class Group(models.Model):
    pass
