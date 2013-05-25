from setuptools import setup, find_packages
from cfd import __version__ as version
import os
root = lambda f: os.path.join(os.path.dirname(os.path.abspath(__file__)), f)

setup(
    name = 'cfd',
    version = version,
    description = open(root('README.md')),
    author = 'Kristian Oellegaard',
    author_email = 'kristian@oellegaard.com',
    url = 'https://github.com/KristianOellegaard/cfd',
    packages = find_packages(
        exclude = [
            'cfd_example',
            'cfd_nginx',
        ],
    ),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        open(root('requirements.txt')).readlines(),
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    license='apache',
    entry_points={
        'console_scripts': [
            'cfd-server = cfd_server.server:run',
            'cfd-agent = cfd_agent.agent:run_agent',
            'cfd-manage = manage:run',
        ]
    },
)
