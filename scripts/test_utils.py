import os
import subprocess


def basic_setup(hostname):
    hostname_setup(hostname)
    subprocess.check_call(['apt-get', 'update'])
    subprocess.check_call(['/usr/bin/sudo', '/usr/bin/apt-get', 'install', '-q', '-y', 'python-setuptools',
                           'build-essential', 'python-dev', 'facter', 'avahi-daemon', 'mdns-scan'])
    subprocess.check_call(['/usr/bin/sudo', '/usr/bin/python', 'setup.py', 'develop'], cwd="/var/lib/cfd/")
    ensure_dir('/etc/cfd/')


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def hostname_setup(hostname):
    with open('/etc/hostname', 'w') as f:
        f.write(hostname)
    with open("/etc/hosts", "a") as f:
        f.write("127.0.1.1	%s" % hostname)
    subprocess.check_call(['hostname', '-F', '/etc/hostname'])