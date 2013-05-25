#!/usr/bin/env python
from test_utils import basic_setup, ensure_dir, hostname_setup

basic_setup()

with open('/etc/cfd/config.yaml', 'w+') as f:
    f.write("""---
    server: 10.0.0.1
    api_key: abcdef
""")
hostname_setup("server-1.testorg.org")