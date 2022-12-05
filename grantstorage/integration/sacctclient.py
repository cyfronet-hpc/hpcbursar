# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

import subprocess
from django.conf import settings
from datetime import datetime, timedelta


class SacctClient(object):
    def __init__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.sacct_path = settings.SLURM_SACCT_LOCATION

    def execute(self, cmd, override=False):
        cmd_full = [self.sacct_path, "-P"] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, stdout=subprocess.PIPE, text=True)
            return cp.returncode, cp.stdout, cp.stderr
        return 0, "", ""

    def get_jobs_acct(self, start, end):
        fields = ['JobID', 'User', 'Group', 'Account', 'ReservationId', 'Partition', 'Submit', 'Start', 'End',
                  'NodeList', 'CPUTimeRAW', 'ElapsedRaw', 'MaxRSS', 'ExitCode', 'NCPUS', 'AllocTres']

        command = [
            'sacct', '-D', '-P', '-X',
            '-s', 'BF,CA,CD,F,NF,OOM,PR,TO,DL,RQ',
            '-S', start,
            '-E', end,
            '--noconvert',
            '--format',
            ",".join(fields)
        ]
        return_code, output, stderr = self.execute(command)
        jobs = []
        for line in output.split('\n'):
            job = dict(zip([field.lower() for field in fields], line.split('|')))
            jobs += [job]

        return jobs
