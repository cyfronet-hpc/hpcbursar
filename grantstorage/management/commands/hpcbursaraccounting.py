from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage

class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def calculate_allocations(self):
        pass

    def handle(self, *args, **options):
        ms = MongoStorage()

