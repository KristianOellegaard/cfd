
class AlreadyRegisteredException(Exception):
    pass

class CFDPool(dict):
    """
    A pool you can register components in. Quite similar to the way models are registered in the django admin. It
    takes an object and a 'name' for it. The name can later be used to access the object again::

        pool = CFDPool()
        pool.register(object(), 'specific_object')
        pool.get('specific_object') == pool['specific_object']

    """
    def register(self, itm, name=None):
        name = name or itm.__name__
        if name in self:
            raise AlreadyRegisteredException("%s already registered" % name)
        self[name] = itm

node_registry = CFDPool()
function_registry = CFDPool()