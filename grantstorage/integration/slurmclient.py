import subprocess
from django.conf import settings


class SacctmgrException(Exception):
    pass


class SacctmgrClient(object):
    def __init__(self):
        self.verbose = settings.SLURM_CLIENT_VERBOSE
        self.dryrun = False
        self.sacctmgr_path = settings.SLURM_SACCTMGR_LOCATION

    def execute(self, cmd, override=False):
        cmd_full = [self.sacctmgr_path, '-iP'] + cmd
        if self.verbose:
            print('Executing command: %s' % str(cmd_full))
        if not self.dryrun or override:
            cp = subprocess.run(cmd_full, capture_output=True)
            # output is converted to utf8 string!
            return cp.returncode, cp.stdout.decode(), cp.stderr.decode()
        return 0, '', ''

    # adds
    def add_account(self, name, fairshare=0):
        cmd = ['add', 'account', name, 'fairshare=' + str(fairshare)]
        self.execute(cmd)

    def add_user_account(self, login, account):
        cmd = ['add', 'user', login, 'account=' + account]
        self.execute(cmd)

    # updates
    def update_user_default_account(self, login, account):
        cmd = ['update', 'user', 'name=' + login, 'set defaultaccount=' + account]
        self.execute(cmd)

    def update_user_account_maxsubmit(self, login, account, maxsubmit):
        cmd = ['update', 'user', 'name=' + login, 'account=' + account, 'set maxsubmit=' + str(maxsubmit)]
        self.execute(cmd)

    def update_user_maxsubmit(self, login, maxsubmit):
        cmd = ['update', 'user', 'name=' + login, 'set maxsubmit=' + str(maxsubmit)]
        self.execute(cmd)

    def update_account_maxsubmit(self, account, maxsubmit):
        cmd = ['update', 'account', 'name=' + account, 'set maxsubmit=' + str(maxsubmit)]
        self.execute(cmd)

    def update_account_fairshare(self, account, fairshare):
        cmd = ['update', 'account', 'name=' + account, 'set fairshare=' + str(fairshare)]
        self.execute(cmd)

    # remove
    def remove_account(self, account):
        cmd = ['remove', 'account', 'name=' + account]
        self.execute(cmd)

    def remove_user(self, login):
        cmd = ['remove', 'user', 'name=' + login]
        self.execute(cmd)

    def remove_user_account(self, login, account):
        cmd = ['remove', 'user', 'name=' + login, 'account=' + account]
        self.execute(cmd)

    # gets
    def get_user_default_account_dict(self):
        cmd = ['show', 'users', 'format=user,defaultaccount']
        err, stdout, stderr = self.execute(cmd, True)
        user_dict = {}
        for line in stdout.split('\n')[1:]:
            if not line:
                continue
            user, account = line.split('|')
            user_dict[user] = account
        return user_dict

    def get_account_list(self):
        cmd = ['show', 'accounts']
        err, stdout, stderr = self.execute(cmd, True)
        account_list = []
        for line in stdout.split('\n')[1:]:
            if not line:
                continue
            account, *_ = line.split('|')
            account_list += [account]
        return account_list

    def get_assoc_dict(self):
        cmd = ['show', 'assoc', 'format=account,user,share,maxsubmit']
        err, stdout, stderr = self.execute(cmd, True)
        assoc_dict = {}
        for line in stdout.split('\n')[1:]:
            if not line:
                continue
            account, user, fairshare, maxsubmit = line.split('|')
            if account not in assoc_dict.keys():
                assoc_dict[account] = {'users': {}}

            if not user:
                assoc_dict[account]['fairshare'] = int(fairshare)
                assoc_dict[account]['maxsubmit'] = int(maxsubmit) if maxsubmit else None
            else:
                assoc_dict[account]['users'][user] = {
                    'share': int(fairshare),
                    'maxsubmit': int(maxsubmit) if maxsubmit else None
                }

        return assoc_dict
