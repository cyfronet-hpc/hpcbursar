import subprocess
from django.conf import settings


class SacctAllocationClient(object):
    PER_ALLOCATION = {
        "MEM_PER_GPU": 384 / 8,
        "CPU_PER_GPU": 36 / 8,
        "MEM_PER_CPU": 192 / 48,
        "MEM_PER_CPU_BIG_MEM": 384 / 48
    }

    PARTITION_ALLOCATION_MAP = {
        "plgrid-gpu-v100": "GPU",
        "plgrid": "CPU",
        "plgrid-long": "CPU",
        "plgrid-bigmem": "CPU_BIG_MEM"
    }

    UNIT_FACTOR = {
        "K": 0.000001,
        "M": 0.001,
        "G": 1,
        "T": 1000
    }

    def __int__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.sacctmgt_path = settings.SLURM_SACCTMGR_LOCATION

    def execute(self, cmd, override=False):
        cmd_full = [self.sacctmgt_path, "-iP"] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, stdout=subprocess.PIPE, text=True)
            return cp.returncode, cp.stdout, cp.stderr
        return 0, "", ""

    def sacct_command(self, start, end):
        command = f"sacct -D -P -X -s 'BF,CA,CD,F,NF,OOM,PR,TO,DL,RQ' -S{start} -E{end} --format JobID,User,Group,Account,ReservationId,Partition,Submit,Start,End,NodeList,CPUTimeRAW,ElapsedRaw,MaxRSS,ExitCode,NCPUS,ReqTRES"
        command = command.split()
        return_code, output, stderr = self.execute(command)
        if stderr:
            raise Exception("Cannot run a command.\n")
        output = output.split()
        cost = 0
        for i in range(1, len(output)):
            split_alloc = output[i].split("|")
            allocation_type = self.PARTITION_ALLOCATION_MAP[split_alloc[5]]
            elapsed_raw = split_alloc[11]
            req_tres = split_alloc[15]
            price = self.parse_req_tres(req_tres, allocation_type)
            cost += int(elapsed_raw) / 3600 * price
        return cost

    def parse_req_tres(self, req_tres, allocation_type):
        parsed_req_tres = req_tres.split(",")
        gpu = cpu = memory = ""
        for rt in parsed_req_tres:
            if rt.find("gpu") != -1:
                gpu_values = rt.split("=")
                gpu = int(gpu_values[-1])
            elif rt.find("cpu") != -1:
                cpu_values = rt.split("=")
                cpu = int(cpu_values[-1])
            elif rt.find("mem") != -1:
                memory_values = rt.split("=")
                memory = self.convert_to_megabytes(memory_values[-1])
        if allocation_type == "GPU":
            return self.calculate_gpu_price(gpu, cpu, memory)
        elif allocation_type == "CPU":
            return self.calculate_cpu_price(cpu, memory)
        elif allocation_type == "CPU_BIG_MEM":
            return self.calculate_cpu_big_mem_price(cpu, memory)
        return 0

    def calculate_gpu_price(self, gpu, cpu, memory):
        return max(gpu, memory / self.PER_ALLOCATION["MEM_PER_GPU"], cpu / self.PER_ALLOCATION["CPU_PER_GPU"])

    def calculate_cpu_price(self, cpu, memory):
        return max(cpu, memory / self.PER_ALLOCATION["MEM_PER_CPU"])

    def calculate_cpu_big_mem_price(self, cpu, memory):
        return max(cpu, memory / self.PER_ALLOCATION["MEM_PER_CPU_BIG_MEM"])

    def convert_to_megabytes(self, memory_allocation):
        unit = memory_allocation[-1]
        if '0' <= unit <= "9":
            unit = ""
        factor = self.UNIT_FACTOR[unit]
        memory_allocation = int(memory_allocation[:-1])
        return memory_allocation * factor
