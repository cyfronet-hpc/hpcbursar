ALLOWED_HOSTS = ['127.0.0.1', 'slurm01.ares.cyfronet.pl']

GRID_CERTIFICATE_LOCATION = 'path to your .pem file'
GRID_KEY_LOCATION = 'path to your .key file'

PLGRID_PORTAL_URL = 'https://portal.plgrid.pl/'
PLGRID_SITE_NAME = 'CYFRONET-ARES'

PLG_LOGIN_PREFIX = 'plg'
PLG_ACCOUNT_PREFIX = 'plg'

SLURM_CLUSTER_NAME = 'ares'
SLURM_CLIENT_VERBOSE = True
SLURM_SACCTMGR_LOCATION = '/opt/slurm/releases/production/bin/sacctmgr'
SLURM_SCONTROL_LOCATION = '/opt/slurm/releases/production/bin/scontrol'

SLURM_SUPPORTED_RESOURCES = ['CPU', 'GPU']
SLURM_RESOURCE_PARTITION_MAPPING = {
    'CPU': 'plgrid',
    'GPU': 'plgrid-gpu-v100'
}
SLURM_ACL_PLACEHOLDER = 'hpcb'

SLURM_ADMIN_USER = 'admin user'
