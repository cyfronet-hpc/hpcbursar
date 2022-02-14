import subprocess
from django.conf import settings


class ScontrolException(Exception):
    pass


class ScontrolClient(object):
    def __init__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.scontrol_path = settings.SLURM_SCONTROL_LOCATION
        self.acl_placeholder = settings.SLURM_ACL_PLACEHOLDER

    def execute(self, cmd, override=False):
        cmd_full = [self.scontrol_path] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, capture_output=True)
            # output is converted to utf8 string!
            return cp.returncode, cp.stdout.decode(), cp.stderr.decode()
        return 0, '', ''

    # sets
    def set_partition_accounts(self, partition_name, accounts):
        current_accounts = self.get_partition_accounts_raw(partition_name)
        if current_accounts.count(self.acl_placeholder) == 2:
            start = current_accounts.index(self.acl_placeholder)
            end = current_accounts.index(self.acl_placeholder, start + 1) + 1
            prefix_accounts = current_accounts[:start]
            postfix_accounts = current_accounts[end:]
            new_accounts = prefix_accounts + [self.acl_placeholder] + accounts + [self.acl_placeholder] \
                           + postfix_accounts
            self.set_partition_accounts_raw(partition_name, new_accounts)
        elif current_accounts.count(self.acl_placeholder) == 0:
            new_accounts = current_accounts + [self.acl_placeholder] + accounts + [self.acl_placeholder]
            self.set_partition_accounts_raw(partition_name, new_accounts)
        else:
            raise ScontrolException('Unsupported placeholder configuration!')

    def set_partition_accounts_raw(self, partition_name, accounts):
        cmd = ['update', 'partition=' + partition_name, 'allowaccounts=' + ','.join(accounts)]
        self.execute(cmd)

    # gets
    def get_partition_accounts_raw(self, partition_name):
        cmd = ['show', 'partition=' + partition_name]
        err, stdout, stderr = self.execute(cmd)
        for line in stdout.split('\n'):
            if 'AllowAccounts' in line:
                parts = line.split()
                for part in parts:
                    if 'AllowAccounts' in part:
                        _, accounts_raw = part.split('=')
                        accounts = accounts_raw.split(',')
                        return accounts
        return []

    def get_partition_accounts(self, partition_name):
        accounts_raw = self.get_partition_accounts_raw(partition_name)
        if accounts_raw.count(self.acl_placeholder) == 2:
            start = accounts_raw.index(self.acl_placeholder) + 1
            end = accounts_raw.index(self.acl_placeholder, start)
            return accounts_raw[start:end]
        return []
