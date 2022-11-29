# HPCBursar

Slurm account management based on concept of 'grants'.

# Installation requirements
 * python3 in modern version is required, preferably RHEL8/9 based system
 * dedicated virtual environment for python application
 * requirements from `requirements.txt`
 * mongodb running on the localhost
 * munge enabled cluster
 * websever such as httpd for hosting services


# Installation
 * Main hpcbursar installation should be done on the slurm host. This machine will serve the apis used by other tools, namely 'hpcbursarcli'. HTTP APIs should be accessible from the cluster network.
 * Deploy the main Django webapp: https://docs.djangoproject.com/en/4.0/howto/deployment/
 * Set the GRID_, EC_, PLGRID_, PLG_, SLURM_, variables in settings.py file, according to your specific site configuration. Please contact PLGrid CO for clarification on accessing the Portal APIs.
 * Create a cronjob to periodically execute the downloadgrants, updatepartitions, updateslurmconfig commands, by using the "python manage.py" interface, e.g.:
```
5 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py downloadgrants
11 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py updatepartitions
12 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py updateslurmconfig
```