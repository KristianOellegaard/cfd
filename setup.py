from setuptools import setup, find_packages
from cfd import __version__ as version

setup(
    name = 'cfd',
    version = version,
    description = open('README.md'),
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
        open('requirements.txt').readlines(),
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
        ]
    },
)
