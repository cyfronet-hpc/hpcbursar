from django.db import models


# Grant

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
    end = models.DateTimeField()
    name = models.TextField()
    # ola_list = models.ForeignKey(OlaList, on_delete=models.CASCADE, default=1)
    start = models.DateTimeField()
    state = models.TextField()
    team = models.TextField()


# User
class AffiliationList(models.Model):
    end = models.TextField()
    status = models.TextField()
    type = models.TextField()
    units = models.TextField()


class User(models.Model):
    # affiliation_list = models.ForeignKey(AffiliationList, on_delete=models.CASCADE, default=1)
    email = models.TextField()
    first_name = models.TextField()
    i_d = models.IntegerField()
    last_name = models.TextField()
    login = models.TextField()
    opi = models.TextField()
    service_list = models.TextField()
    status = models.TextField()


# Group
class Group(models.Model):
    description = models.TextField()
    name = models.TextField()
    status = models.TextField()
    teamId = models.TextField()
    teamLeaders = models.TextField()
    teamMembers = models.TextField()
    type = models.TextField()
