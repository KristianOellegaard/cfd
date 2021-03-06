from cfd.modules import CFDModule


class CFDException(Exception):
    pass


class CFDNodeMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        for key, value in future_class_attr.items():
            if key == "modules":
                del future_class_attr[key]
                future_class_attr["modules_%s" % future_class_name.lower()] = value

        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr)


class CFDNode(object):
    """
    Base class for nodes. Nodes inherit from this class or other nodes that eventually inherit from CFDNode.

    Example::

        class InternalServer(CFDNode):
            modules = [
                CFDFile("/etc/motd", content="An Acme Ltd server"),
            ]

        class WebServer(InternalServer):
            modules = [
                Nginx(),  # Use the nginx module with default settings
            ]

        class ASpecificServer(WebServer):
            modules = [
                NginxVirtualHost("domain.com"),
            ]
    """
    __metaclass__ = CFDNodeMetaclass

    def __init__(self, hostname, facts):
        self.hostname = hostname
        self.facts = facts
        self.modules = []

        for method in dir(self):
            if method.startswith("modules_"):
                try:
                    mthd = getattr(self, method)
                    if callable(mthd):
                        mthd = mthd()
                    for item in mthd:
                        self.add(item)
                except Exception as e:
                    raise CFDException(u"%s: %s" % (type(e), e.message))
        if not self.modules:
            raise Exception("Please define at least one module for %s" % hostname)

    def add(self, module):
        self.modules.append(module)

    def as_dict(self):
        return {
            'hostname': self.hostname,
            'facts': self.facts,
            'items': [item.as_dict() for item in self.modules],
        }
