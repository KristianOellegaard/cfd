
class CFDPool(dict):
    def register(self, itm, name=None):
        name = name or itm.__name__
        if name in self:
            raise Exception("%s already registered" % name)
        self[name] = itm

node_registry = CFDPool()
function_registry = CFDPool()