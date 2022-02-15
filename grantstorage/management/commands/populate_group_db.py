from django.core.management.base import BaseCommand
from grantstorage.service.v1.user import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_group()


def create_group():
    group = Group(description="Test description string",
                  name="Test name string",
                  status="Test status string",
                  teamId="Test teamId string",
                  teamLeaders="Test team leaders string",
                  teamMembers="Test team members string",
                  type="Test type string")
    group.save()
