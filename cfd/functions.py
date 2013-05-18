from difflib import context_diff
import subprocess
from cfd.pool import function_registry
import os
import logging

logging.basicConfig()
logger = logging.getLogger("cfd")


def name_decorator(f):
    def inner(*args, **kwargs):
        return_value = f(*args, **kwargs)
        return_value.update(
            {
                'name': args[0].__class__.__name__,  # args[0] will always be self in this case
                'type': 'function'  # args[0] will always be self in this case
            }
        )
        return return_value
    return inner


class CFDFunctionMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        # Introspect model to check it has:
        # enabled=true/false
        if 'as_dict' in future_class_attr:
            future_class_attr['as_dict'] = name_decorator(future_class_attr['as_dict'])
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr)


class CFDFunction(object):
    __metaclass__ = CFDFunctionMetaclass

    def as_dict(self):
        return {}

    def execute(self, facts):
        raise Exception("You must define a execute function on the CFDFunction subclass")


class CFDExecuteCommand(CFDFunction):
    def __init__(self):
        pass


class CFDFile(CFDFunction):
    def __init__(self, path, ensure, content):
        self.path = path
        self.ensure = ensure
        self.content = content

    def as_dict(self):
        return {
            'path': self.path,
            'ensure': self.ensure,
            'content': self.content
        }

    def execute(self, facts):
        if self.ensure:
            try:
                with open(self.path, 'r+') as f:
                    previous_content = f.read()
            except IOError:
                previous_content = ""
            diff = list(context_diff(previous_content.split("\n"), self.content.split("\n"), n=0))
            if diff:
                logger.info("File Changed:\n" + "\n".join(diff))
            try:
                with open(self.path, 'w+') as f:
                    f.write(self.content)
            except IOError:
                logger.warn("Directory does not exist at %s" % self.path)
        else:
            if os.path.exists(self.path):
                logger.info("Removed %s" % self.path)
                os.remove(self.path)


class CFDPackage(CFDFunction):
    def __init__(self, package_name, ensure=True, package_manager=None):
        self.package_name = package_name
        self.ensure = ensure
        self.package_manager = package_manager

    def as_dict(self):
        return {
            'package_name': self.package_name,
            'package_manager': self.package_manager,
            'ensure': self.ensure
        }

    def execute(self, facts):
        package_manager = self.package_manager
        cmd = None
        if not package_manager:
            if facts['osfamily'] == 'Debian':
                package_manager = 'apt-get'
        if package_manager == 'apt-get':
            cmd = ['apt-get', 'install', '-f', '-y', self.package_name]
        if not cmd:
            raise Exception("Package manager %s not found" % package_manager)
        subprocess.check_call(cmd, stdout=subprocess.PIPE)

function_registry.register(CFDExecuteCommand)
function_registry.register(CFDFile)
function_registry.register(CFDPackage)