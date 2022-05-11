import subprocess

from django.conf import settings


class SacctAllocationClient(object):
    def __int__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.sacctmgt_path = settings.SLURM_SACCTMGR_LOCATION

    def execute(self, cmd, override=False):
        cmd_full = [self.sacctmgt_path, "-iP"] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, capture_output=True)
            return cp.returncode, cp.stdout.decode(), cp.stderr.decode()
        return 0, "", ""

    # sacct -X -D
    def example_cmd(self):
        cmd = ["-X", "-D"]
        self.execute(cmd)
