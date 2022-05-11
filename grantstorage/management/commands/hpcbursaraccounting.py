from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.integration.sacctallocationintegration import SacctAllocationClient


class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctAllocationClient()

    def calculate_allocations(self):
        pass

    def handle(self, *args, **options):
        # TODO handle not finished yet
        self.setup()

        groups = self.ms.find_groups_by_member()
        allocation_usages = self.ms.find_allocation_usages_by_group(groups)

        self.ms.store_allocation_usages(allocation_usages)
