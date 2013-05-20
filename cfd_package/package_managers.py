import subprocess
from cfd.pool import CFDPool

package_manager_registry = CFDPool()


class CFDPackageManager(object):
    def latest_version(self, package):
        """
        Show the latest version for `package`
        """
        raise Exception("Please define an latest_version method on your package manager %s" % self.__class__.__name__)

    def list_installed_packages(self):
        """
        List all installed packages
        """
        raise Exception("Please define an list_packages method on your package manager %s" % self.__class__.__name__)

    def version(self, package):
        """
        Return package version or None if not installed
        """
        raise Exception("Please define an version method on your package manager %s" % self.__class__.__name__)

    def install(self, package, version=None):
        """
        Install a package, optionally a specific version
        """
        raise Exception("Please define an install method on your package manager %s" % self.__class__.__name__)

    def uninstall(self, package):
        """
        Uninstall package but leave config files etc.
        """
        raise Exception("Please define an uninstall method on your package manager %s" % self.__class__.__name__)

    def remove(self, package):
        """
        Completely remove package and configuration
        """
        raise Exception("Please define an remove method on your package manager %s" % self.__class__.__name__)

    def refresh_db(self):
        """
        Refresh the package db
        """
        raise Exception("Please define an refresh_db method on your package manager %s" % self.__class__.__name__)


class AptGetPackageManager(CFDPackageManager):
    def version(self, package):
        return False

    def install(self, package, version=None):
        subprocess.check_call(['apt-get', '-q', '-y', 'install', package], stdout=subprocess.PIPE)

    def uninstall(self, package):
        subprocess.check_call(['apt-get', '-q', '-y', 'remove', package], stdout=subprocess.PIPE)

    def remove(self, package):
        subprocess.check_call(['apt-get', '-q', '-y', 'purge', package], stdout=subprocess.PIPE)

package_manager_registry.register(AptGetPackageManager, 'apt-get')


class PipPackageManager(CFDPackageManager):

    def list_installed_packages(self):
        packages = subprocess.check_output(['pip', 'freeze'])
        return [pkg.split("==")[0] for pkg in packages.split("\n")]

    def version(self, package):
        packages = subprocess.check_output(['pip', 'freeze'])
        return ([pkg.split("==")[1] for pkg in packages.split("\n") if pkg.split("==")[0] == package] or [None])[0]

    def install(self, package, version=None):
        if version:
            subprocess.check_call(['pip', 'install', '-q', '%s==%s' % (package, version)], stdout=subprocess.PIPE)
        else:
            subprocess.check_call(['pip', 'install', '-q', package], stdout=subprocess.PIPE)

    def uninstall(self, package):
        subprocess.check_call(['pip', 'uninstall', '-q', '-y', package], stdout=subprocess.PIPE)

package_manager_registry.register(PipPackageManager, 'pip')