# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.integration.sacctclient import SacctAllocationClient




class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctAllocationClient()

    # def get_current_hour():
    #     now = datetime.now().replace(minute=0, second=0, microsecond=0)
    #     return now.strftime("%H:%M:%S")
    #
    # def get_previous_hour():
    #     now = datetime.now().replace(minute=0, second=0, microsecond=0)
    #     hour_before = now - timedelta(hours=1)
    #     return hour_before.strftime("%H:%M:%S")

    def handle(self, *args, **options):
        # TODO handle not finished yet
        pass
        # self.setup()
        # member = args
        # groups = self.ms.find_groups_by_member(member)
        # for g in groups:
        #     allocation_usage = self.ms.find_allocations_by_group(g)
        #     self.ms.store_allocation_usage(allocation_usage)
        #
        # self.sc.sacct_command()
