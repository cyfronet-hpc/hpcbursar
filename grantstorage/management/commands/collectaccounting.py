# Copyright 2022 ACC Cyfronet AGH-UST
import json

import pytz
# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.core.management.base import BaseCommand
from grantstorage.storage.mongo.mongostorage import MongoStorage
from grantstorage.localmodels.allocationusage import AllocationUsage, Summary, Usage
from grantstorage.integration.sacctclient import SacctClient
from datetime import datetime, timedelta
from django.conf import settings


class Command(BaseCommand):
    help = "Calculate total user usage of allocations"

    pltz = pytz.timezone('Europe/Warsaw')

    def setup(self):
        self.ms = MongoStorage()
        self.sc = SacctClient()

    def calculate_job_billing(self, job):
        alloctres = job['alloctres']
        partition = job['partition']
        elapsedraw = job['elapsedraw']
        allocation = job['account']

        elapsed_hours = int(elapsedraw) / 3600.

        resources = {}
        for resource_amounts in alloctres.split(','):
            resource, amount = resource_amounts.split('=')
            if resource == 'mem':
                if amount[-1] != 'M':
                    print('Warning! Unknown memory unit!')
                amount = amount[:-1]
            resources[resource] = int(amount)

        billing_info = settings.PARTITION_BILLING.get(partition, {'billed_resource': None})

        job_billing = {}
        if billing_info['billed_resource'] == 'cpu':
            tokens_cpu = elapsed_hours * resources['cpu']
            tokens_mem = elapsed_hours * resources['mem'] / billing_info['mem']
            job_billing['cpu'] = max(tokens_cpu, tokens_mem)
        elif billing_info['billed_resource'] == 'gres/gpu':
            tokens_gpu = elapsed_hours * resources['gres/gpu']
            tokens_cpu = elapsed_hours * resources['cpu'] / billing_info['cpu']
            tokens_mem = elapsed_hours * resources['mem'] / billing_info['mem']
            job_billing['gres/gpu'] = max(tokens_gpu, tokens_cpu, tokens_mem)
        else:
            print('Warning! Unknown resource')

        return allocation, job_billing

    # TODO: this assumes that usages use only a single key!
    def sum_usages(self, usages):
        key = list(usages[0].resources.keys())[0]
        result = {key: sum(map(lambda usage: usage.resources[key], usages))}
        return result

    def update_allocation_usage(self, allocation, billing, start, end):
        now = datetime.now(tz=self.pltz)
        allocation_usage = self.ms.find_allocation_usage_by_name(allocation)
        if not allocation_usage:
            summary = Summary(timestamp=now, resources=billing)
            usage = Usage(timestamp=now, start=start, end=end, resources=billing)
            allocation_usage = AllocationUsage(name=allocation, summary=summary, usages=[usage])
        else:
            summary = allocation_usage.summary
            usages = list(filter(lambda usage: usage.start != start, allocation_usage.usages.copy()))
            usages += [Usage(timestamp=now, start=start, end=end, resources=billing)]

            summary.timestamp = now
            summary.resources = self.sum_usages(usages)
            # print(summary)

            allocation_usage.summary = summary
            allocation_usage.usages = usages

        print(allocation_usage)
        self.ms.store_allocation_usage(allocation_usage)

    def add_arguments(self, parser):
        parser.add_argument('start_timestamp', nargs='?', default=None)

    def sum_dicts(self, a, b):
        keys = set(set(a.keys()) + set(b.keys()))
        result = {}
        for key in keys:
            result[key] = a.get(key, 0) + b.get(key, 0)
        return result

    def handle(self, *args, **options):
        self.setup()

        period_start_date = datetime.now(tz=self.pltz).replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
        if options['start_timestamp'] is not None:
            period_start_date = self.pltz.localize(datetime.strptime(options['start_timestamp'], '%Y-%m-%dT%H:%M:%S'))
        period_end_date = period_start_date + timedelta(minutes=59, seconds=59)

        jobs = self.sc.get_jobs_acct(period_start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                                     period_end_date.strftime("%Y-%m-%dT%H:%M:%S"))

        allocation_billing = {}
        for job in jobs:
            allocation, job_billing = self.calculate_job_billing(job)
            if allocation in allocation_billing.keys():
                allocation_billing[allocation] = self.sum_dicts(allocation_billing[allocation], job_billing)
            else:
                allocation_billing[allocation] = job_billing

        for allocation, billing in allocation_billing.items():
            print(f"Updating billing information for: {allocation} {billing}")
            self.update_allocation_usage(allocation, billing, period_start_date, period_end_date)
