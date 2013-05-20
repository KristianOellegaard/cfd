
class CFDModuleMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        # Introspect model to check it has:
        # enabled=true/false
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr)


class CFDModule(object):
    """
    Base class for modules
    """
    __metaclass__ = CFDModuleMetaclass

    def __init__(self):
        self.items = []

    def add(self, *items):
        try:
            getattr(self, 'items')
        except AttributeError:
            raise Exception("Module.functions is missing. Please check you called super()")
        for function in items:
            self.items.append(function)

    def as_dict(self):
        return {
            'name': self.__class__.__name__,
            'type': 'module',
            'items': [f.as_dict() for f in self.items]
        }
