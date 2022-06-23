import subprocess

from django.conf import settings


class SacctAllocationClient(object):
    PER_ALLOCATION = {
        "MEM_PER_GPU": 384 / 8,
        "CPU_PER_GPU": 36 / 8,
        "MEM_PER_CPU": 192 / 48,
        "MEM_PER_CPU_BIG_MEM": 384 / 48
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

    def parse_req_tres(self, req_tres):
        parsed_req_tres = req_tres.split(",")
        gpu = cpu = memory = ""
        for rt in parsed_req_tres:
            if rt.find("gpu"):
                gpu_values = rt.split("=")
                gpu = gpu_values[-1][:-1]
            elif rt.find("cpu"):
                cpu_values = rt.split("=")
                cpu = cpu_values[-1][:-1]
            elif rt.find("mem"):
                memory_values = rt.split("=")
                memory = memory_values[-1]
        gpu_price = self.calculate_gpu_price(gpu, cpu, memory)
        cpu_price = self.calculate_cpu_price(cpu, memory)
        cpu_big_mem_price = self.calculate_cpu_big_mem_price(cpu, memory)
        return gpu_price + cpu_price + cpu_big_mem_price

    def calculate_gpu_price(self, gpu, cpu, memory):
        return max(gpu, memory / self.PER_ALLOCATION["MEM_PER_GPU"], cpu / self.PER_ALLOCATION["CPU_PER_GPU"])

    def calculate_cpu_price(self, cpu, memory):
        return max(cpu, memory / self.PER_ALLOCATION["MEM_PER_CPU"])

    def calculate_cpu_big_mem_price(self, cpu, memory):
        return max(cpu, memory / self.PER_ALLOCATION["MEM_PER_CPU_BIG_MEM"])

    def sacct_command(self):
        start = "10:00:00"
        end = "13:00:00"
        command = f"sacct -D -P -X -s 'BF,CA,CD,F,NF,OOM,PR,TO,DL,RQ' -S{start} -E{end} --format JobID,User,Group,Account,ReservationId,Partition,Submit,Start,End,NodeList,CPUTimeRAW,ElapsedRaw,MaxRSS,ExitCode,NCPUS,ReqTRES"
        command = command.split()
        return_code, output, stderr = self.execute(command)
        if stderr:
            raise Exception("Cannot run a command.\n")
        output = output.split()
        cost = 0
        for i in range(1, len(output)):
            split_alloc = output[i].split("|")
            elapsed_raw = split_alloc[11]
            req_tres = split_alloc[15]
            price = self.parse_req_tres(req_tres)
            cost += int(elapsed_raw) / 3600 * price
        return cost
