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


class CFDTypeMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        # Introspect model to check it has:
        # enabled=true/false
        if 'as_dict' in future_class_attr:
            future_class_attr['as_dict'] = name_decorator(future_class_attr['as_dict'])
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr)


class CFDType(object):
    """
    Base class for any type in CFD
    """
    __metaclass__ = CFDTypeMetaclass

    def as_dict(self):
        return {}

    def execute(self, facts):
        raise Exception("You must define a execute function on the CFDType subclass")


class CFDExecuteCommand(CFDType):
    def __init__(self):
        pass


class CFDFile(CFDType):
    """
    CFDFile is a CFD type that will place a file on the hosts, to which it is assigned.

    Example::

        CFDFile("/etc/motd", content="Welcome to the server", ensure=True)
    """
    def __init__(self, path, content, ensure=True):
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


function_registry.register(CFDExecuteCommand)
function_registry.register(CFDFile)