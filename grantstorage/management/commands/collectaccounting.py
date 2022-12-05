# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.integration.sacctclient import SacctClient
from datetime import datetime, timedelta




class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctClient()

    def get_current_hour(self):
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        return now.strftime("%H:%M:%S")

    def get_previous_hour(self):
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        previous_hour = now - timedelta(hours=1)
        return previous_hour.strftime("%H:%M:%S")

    def handle(self, *args, **options):
        self.setup()

        jobs = self.sc.get_jobs_acct(self.get_current_hour(), self.get_previous_hour())

        print(jobs)
