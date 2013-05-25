import subprocess
import requests
import socket
import yaml
from cfd.pool import function_registry
import os

import logging

logging.basicConfig()
logger = logging.getLogger("cfd")
logger.setLevel(logging.DEBUG)


def run_agent():
    data = yaml.safe_load(subprocess.check_output(['/usr/bin/facter', '--yaml']))
    hostname = socket.gethostname()
    with open("/etc/cfd/config.yaml") as f:
        config = yaml.safe_load(f)
        assert 'api_key' in config, "Please provide api_key in /etc/cfd/config.yaml"
    cfd_server = config.get('server', os.environ.get('CFD_SERVER', "http://localhost:8000/"))
    r = requests.post(
        cfd_server + "%s/" % hostname,
        data=data, headers={'Accept': 'application/json', 'APIKEY': config['api_key']}
    )

    def traverse_items(dct, path=list()):
        if 'items' in dct:
            items = []
            path.append(dct.get('name', hostname))  # Outer item doesn't have `name`, so use hostname
            for item in dct.get('items'):
                value = traverse_items(item, path)
                if type(value) == list:
                    items += value
                else:
                    items.append(value)
            return items
        else:
            dct['item_path'] = " -> ".join(path + [dct['name']])
            return dct

    try:
        json_data = r.json()
    except ValueError:
        print r.text
        exit(1)
        return
    for item in traverse_items(json_data):
        kwargs = item.copy()
        name = kwargs.pop("name")
        typ = kwargs.pop("type")
        path = kwargs.pop("item_path")
        logger.info(path)
        function_registry[item['name']](**kwargs).execute(r.json()['facts'])

if __name__ == "__main__":
    run_agent()