from cfd.pool import function_registry
from cfd.types import CFDType
from cfd_package.package_managers import package_manager_registry


class CFDPackage(CFDType):
    def __init__(self, package_name, ensure=True, package_manager=None, version=None):
        self.package_name = package_name
        self.ensure = ensure
        self.package_manager = package_manager
        self.version = version

    def as_dict(self):
        return {
            'package_name': self.package_name,
            'package_manager': self.package_manager,
            'ensure': self.ensure
        }

    def execute(self, facts):
        package_manager = self.package_manager
        if not package_manager:
            if facts['osfamily'] == 'Debian':
                package_manager = 'apt-get'

        package_manager_class = package_manager_registry[package_manager]()
        if self.ensure:
            package_manager_class.install(self.package_name, version=self.version)
        else:
            package_manager_class.uninstall(self.package_name)

function_registry.register(CFDPackage)