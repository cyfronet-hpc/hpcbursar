from django.core.management.base import BaseCommand
from grantstorage.service.user.user_grant_info import Grant, OlaList
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_grant()


def create_ola_list():
    ola_list = OlaList(createdAt=datetime.now(),
                       end=datetime.now(),
                       grantName="Test grant name string",
                       provider="Test provider string",
                       resource="Test resource string",
                       resources="Test resources string",
                       site="Test site string",
                       start=datetime.now())
    ola_list.save()
    return ola_list


def create_grant():
    grant = Grant(description="Test description string",
                  end=datetime.now(),
                  name="Test name string",
                  # ola_list=create_ola_list(),
                  start=datetime.now(),
                  state="Test state string",
                  team="Test team string")
    grant.save()
