from django.core.management.base import BaseCommand
from grantstorage.models import User, AffiliationList


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_user()


def create_affiliation():
    affiliation = AffiliationList(end="Test end string",
                                  status="Test status string",
                                  type="Test type string",
                                  units="Test units string")
    affiliation.save()
    return affiliation


def create_user():
    user = User(  # affiliation_list=create_affiliation(),
        email="Test email string",
        first_name="Test first name string",
        i_d=0,
        last_name="Test last name string",
        login="Test login string",
        opi="Test opi string",
        service_list="Test service list string",
        status="Test status string")
    user.save()
