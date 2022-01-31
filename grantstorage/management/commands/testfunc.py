from django.core.management.base import BaseCommand, CommandError
import json
from grantstorage.localmodels.user import User, UserSerializer
from rest_framework.renderers import JSONRenderer


class Command(BaseCommand):
    help = 'Test some functionality'

    def handle(self, *args, **options):
        user = User(login="plgpawlik", status="active")
        us = UserSerializer(user)
        self.stdout.write(str(JSONRenderer().render(us.data)))
