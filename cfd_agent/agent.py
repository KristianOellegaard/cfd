import subprocess
import requests
import socket
import yaml
from cfd.pool import function_registry
import os

import logging

logger = logging.getLogger("cfd")
logger.setLevel(logging.DEBUG)
# print function_registry.items
data = yaml.safe_load(subprocess.check_output(['/usr/bin/facter', '--yaml']))
r = requests.post(os.environ.get('CFD_SERVER', "http://localhost:8000/") + "%s/" % socket.getfqdn(), data=data)

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

for item in traverse_items(r.json()):
    kwargs = item.copy()
    kwargs.pop("name")
    kwargs.pop("type")
    function_registry[item['name']](**kwargs).execute(r.json()['facts'])