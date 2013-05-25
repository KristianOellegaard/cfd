#!/usr/bin/env python
import sys
sys.path.append("/vagrant/scripts/")

from test_utils import basic_setup, hostname_setup
import subprocess

basic_setup()
hostname_setup("cfd.testorg.org")

with open('/etc/cfd/server.yaml', 'w+') as f:
    f.write("""---
    DATABASE_URL: sqlite:////etc/cfd/db.sqlite3
""")

subprocess.check_call(['cfd-manage', 'syncdb', '--all', '--noinput'])
subprocess.check_call(['cfd-manage', 'migrate', '--fake'])
api_key = subprocess.check_output(['cfd-manage', 'create_api_key', 'cfd.testorg.org'])

with open('/etc/cfd/config.yaml', 'w+') as f:
    f.write("""---
    server: http://localhost:8000/
    api_key: %s
""" % api_key)

with open('/etc/init/cfd-server.conf', 'w+') as f:
    f.write("""
env DJANGO_SETTINGS_MODULE=cfd_example.settings

exec cfd-server -b 0.0.0.0:8000
""")
subprocess.check_call(['sudo', 'service', 'cfd-server', 'restart'])
subprocess.check_call(['sudo', 'cfd-agent'])