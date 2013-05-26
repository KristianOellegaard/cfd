#!/usr/bin/env python
import sys
sys.path.append("/vagrant/scripts/")

import subprocess
from test_utils import basic_setup, ensure_dir, hostname_setup

basic_setup("server-1.testorg.org")
subprocess.check_call(['sudo', 'cfd-agent'])