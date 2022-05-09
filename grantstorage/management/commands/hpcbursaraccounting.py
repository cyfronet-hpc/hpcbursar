from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.integration.sacctmgrclient import SacctmgrClient


class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctmgrClient()

    def calculate_allocations(self):
        pass

    def handle(self, *args, **options):
        self.setup()

