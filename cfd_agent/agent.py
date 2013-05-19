import subprocess
import requests
import socket
import yaml
from cfd.pool import function_registry
import os

import logging

logger = logging.getLogger("cfd")
logger.setLevel(logging.DEBUG)
data = yaml.safe_load(subprocess.check_output(['/usr/bin/facter', '--yaml']))
with open("/etc/cfd/config.yaml") as f:
    config = yaml.safe_load(f)
    assert 'api_key' in config, "Please provide api_key in /etc/cfd/config.yaml"
r = requests.post(
    os.environ.get('CFD_SERVER', "http://localhost:8000/") + "%s/" % socket.getfqdn(),
    data=data, headers={'Accept': 'application/json', 'APIKEY': config['api_key']}
)

fqdn = socket.getfqdn()


def traverse_items(dct):
    if dct.get('items'):
        items = []
        for item in dct.get('items'):
            value = traverse_items(item)
            if type(value) == list:
                items += value
            else:
                items.append(value)
        return items
    else:
        return dct

try:
    json_data = r.json()
except ValueError:
    print r.text
    exit(1)
for item in traverse_items(json_data):
    kwargs = item.copy()
    kwargs.pop("name")
    kwargs.pop("type")
    function_registry[item['name']](**kwargs).execute(r.json()['facts'])