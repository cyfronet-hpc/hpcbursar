# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

import subprocess
from django.conf import settings
from datetime import datetime, timedelta


class SacctAllocationClient(object):
    def __init__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.sacct_path = settings.SLURM_SACCT_LOCATION

    COLUMN_MAP = {}

    def execute(self, cmd, override=False):
        cmd_full = [self.sacct_path, "-P"] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, stdout=subprocess.PIPE, text=True)
            return cp.returncode, cp.stdout, cp.stderr
        return 0, "", ""

    def sacct_command(self, start, end):
        command = [
            'sacct', '-D', '-P', '-X',
            '-s', 'BF,CA,CD,F,NF,OOM,PR,TO,DL,RQ',
            '-S', start,
            '-E', end,
            '--noconvert',
            '--format',
            'JobID,User,Group,Account,ReservationId,Partition,Submit,Start,End,NodeList,CPUTimeRAW,ElapsedRaw,MaxRSS,ExitCode,NCPUS,AllocTres'
        ]
        return_code, output, stderr = self.execute(command)
        for line in output.split('\n'):
            pass

        cost = 0
        for i in range(1, len(output)):
            split_alloc = output[i].split("|")
            self.elements_to_job(split_alloc)
            price = self.parse_req_tres()
            cost += int(self.COLUMN_MAP["Elapsed"]) / 3600 * price
        return cost

    def elements_to_job(self, elements):
        self.COLUMN_MAP = {
            "JobID": elements[0],
            "User": elements[1],
            "Group": elements[2],
            "Account": elements[3],
            "ReservationId": elements[4],
            "Partition": elements[5],
            "Submit": elements[6],
            "Start": elements[7],
            "End": elements[8],
            "NodeList": elements[9],
            "CPUTimeRAW": elements[10],
            "Elapsed": elements[11],
            "MaxRSS": elements[12],
            "ExitCode": elements[13],
            "NCPUS": elements[14],
            "ReqTRES": elements[15]
        }

    def parse_req_tres(self):
        parsed_req_tres = self.COLUMN_MAP["ReqTRES"].split(",")
        gpu = cpu = memory = 0
        for rt in parsed_req_tres:
            if rt.find("gpu") != -1:
                gpu_values = rt.split("=")
                gpu = int(gpu_values[-1])
            elif rt.find("cpu") != -1:
                cpu_values = rt.split("=")
                cpu = int(cpu_values[-1])
            elif rt.find("mem") != -1:
                memory_values = rt.split("=")
                # memory = self.convert_to_megabytes(memory_values[-1])
        allocation_type = settings.PARTITION_ALLOCATION_MAP[self.COLUMN_MAP["Partition"]]
        args = {"gpu": gpu,
                "cpu": cpu,
                "memory": memory}
        return self.ALLOC_TYPE_TO_FUNC[allocation_type](args)

    def calculate_gpu_price(args):
        return max(args["gpu"], args["memory"] / settings.PER_ALLOCATION["MEM_PER_GPU"],
                   args["cpu"] / settings.PER_ALLOCATION["CPU_PER_GPU"])

    def calculate_cpu_price(args):
        return max(args["cpu"], args["memory"] / settings.PER_ALLOCATION["MEM_PER_CPU"])

    def calculate_cpu_big_mem_price(args):
        return max(args["cpu"], args["memory"] / settings.PER_ALLOCATION["MEM_PER_CPU_BIG_MEM"])

    ALLOC_TYPE_TO_FUNC = {
        "GPU": calculate_gpu_price,
        "CPU": calculate_cpu_price,
        "CPU_BIG_MEM": calculate_cpu_big_mem_price
    }
