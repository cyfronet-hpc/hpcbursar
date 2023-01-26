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

* Main hpcbursar installation should be done on the slurm host. This machine will serve the apis used by other tools,
  namely 'hpcbursarcli'. HTTP APIs should be accessible from the cluster network.
* Deploy the main Django webapp: https://docs.djangoproject.com/en/4.0/howto/deployment/
* Set the GRID_, EC_, PLGRID_, PLG_, SLURM_, variables in settings.py file, according to your specific site
  configuration. Please contact PLGrid CO for clarification on accessing the Portal APIs.
* Create a cronjob to periodically execute the downloadgrants, updatepartitions, updateslurmconfig commands, by using
  the "python manage.py" interface, e.g.:

```
5 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py downloadgrants
11 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py updatepartitions
12 * * * * root /srv/hpcbursar.venv/bin/python3.9 /srv/hpcbursar/manage.py updateslurmconfig
```

# Description of the project structure

## *hpcbursar* directory

A directory where are the django initial files that were created while running `django-admin startproject` command

#### settings.py

`settings.py` file except the default settings that Django creates while creating a project there are some additional
settings that are needed in **hpcbursar** logic:

- *GRID_CERTIFICATE_LOCATION* and *GRID_KEY_LOCATION* - paths to the grid certification which is used for portal
  authentication
- *EC_PRIVKEY_LOCATION* - path to the private key which is required for portalclient
- *PLGRID_PORTAL_V1_URL* and *PLGRID_PORTAL_V2_URL* - urls to portal v1 and v2
- *PLGRID_SITE_NAMES* - names of plgrid sites
- *PLG_LOGIN_PREFIX* and *PLG_ACCOUNT_PREFIX* - prefixes of plgrid login and account
- *SLURM_CLUSTER_NAME* - name of the cluster that the code is working on
- *SLURM_SACCTMGR_LOCATION*, *SLURM_SCONTROL_LOCATION* and *SLURM_SACCT_LOCATION* -
- *SLURM_SUPPORTED_RESOURCES* - resources that are supported by Slurm that are used to generate slurm sacct
  configuration
- *SLURM_PARTITION_MAPPING* - mappings of partitions that are available when using a specific resources
- *SLURM_ACL_PLACEHOLDER* - placeholder of ACL in Slurm
- *PARTITION_BILLING* - mappings of resources that are available in specific partition

#### urls.py

In this file there are specified url paths to access API for admin and user that we provide.

## *grantstorage* directory

Inside this folder there is a logic behind the project.

### integration

This folder contains integration with `v1` and `v2` plgrid portal. There is also logic for integration with sacct and
scontrol.

### localmodels

`localmodels` directory stores models for grant, group, user and allocationusage.

### management

Inside `management` folder there are special commands for example:

- `collectaccounting` which collects accounting and calculates total user usage of allocation
- `downloadgrants_v1` and `downloadgrants_v2` for downloading grants, groups and users information from PLGrid portal
- `updatepartitions` that generates Slurm sacct configuration based on grant, group, user data
- `updateslurmconfig` this command updates partition based on grant, group, user data

### service

`service` folder contains version 1 (`v1`) of API. It is divided into `admin` API that only admin of this project is
able to access and `user` API which handles information about user's grant info.

### storage

In `storage/mongo` directory there is full logic behind storing users, groups, grants and allocations. We used MongoDB
in particular **pymongo** which is a tool for interacting with MongoDB database from Python.

### tests

Inside tests folder, there are tests for `integration`, `localmodels`, `service` and `storage`.
Run tests:
```
python manage.py test
```
