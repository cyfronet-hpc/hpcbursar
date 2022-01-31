from django.core.management.base import BaseCommand, CommandError
import json


class Command(BaseCommand):
    help = 'Test some functionality'

    def handle(self, *args, **options):
        pass
