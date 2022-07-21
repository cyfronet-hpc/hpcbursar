from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.integration.sacctallocationintegration import SacctAllocationClient


class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctAllocationClient()

    def handle(self, *args, **options):
        # TODO handle not finished yet
        self.setup()
        member = args
        groups = self.ms.find_groups_by_member(member)
        for g in groups:
            allocation_usage = self.ms.find_allocations_by_group(g)
            self.ms.store_allocation_usage(allocation_usage)

        self.sc.sacct_command()
