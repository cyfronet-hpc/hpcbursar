import subprocess
from django.conf import settings


class SacctmgrException(Exception):
    pass


class SacctmgrClient(object):
    def __init__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = True
        self.sacctmgr_path = settings.SLURM_SACCTMGR_LOCATION

    def execute(self, cmd):
        if self.verbose:
            print('Executing command: %s' % str([self.sacctmgr_path, '-iP'] + cmd))
        if not self.dryrun:
            cp = subprocess.run([self.sacctmgr_path, '-iP'] + cmd, capture_output=True)
            return cp.returncode, cp.stdout, cp.stderr
        return 0, '', ''

    def add_account(self, name):
        cmd = ['add', 'account', name]
        self.execute(cmd)

    def add_user(self, login, account):
        cmd = ['add', 'user', login, 'account=' + account]
        self.execute(cmd)

    def get_user_list(self):
        cmd = ['show', 'users']
        err, stdout, stderr = self.execute(cmd)
        user_list = []
        for line in stdout.split('\n')[1:]:
            user, *_ = line.split('|')
            user_list += [user]
        return user_list

    def get_account_list(self):
        cmd = ['show', 'accounts']
        err, stdout, stderr = self.execute(cmd)
        account_list = []
        for line in stdout.split('\n')[1:]:
            account, *_ = line.split('|')
            account_list += [account]
        return account_list

    def get_assoc_dict(self):
        cmd = ['show', 'assoc', 'format=account,user,share,maxsubmit']
        err, stdout, stderr = self.execute(cmd)
        assoc_dict = []
        for line in stdout.split('\n')[1:]:
            account, user, share, maxsubmit = line.split('|')
            if account not in assoc_dict.keys():
                assoc_dict[account] = {}

            if user == '':
                assoc_dict[account]['share'] = share
                assoc_dict[account]['maxsubmit'] = maxsubmit


            assoc_dict[account] = {
                'user': user,
                'share': share,
                'maxsubmit': maxsubmit
            }
        return assoc_dict
