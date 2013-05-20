Tutorial
********

To start using CFD you need to define a few nodes and add types to them. This is done the following way::

    from cfd.types import CFDFile
    from cfd.nodes import CFDNode

    class YourServer(CFDNode):
        """
        You can include any comments here and automatically generate a full documentation of your infrastructure from
        it.
        """
        modules = [
            CFDFile("/etc/motd", content="This is a CFD managed server"),
        ]

You can subclass your new class if you want, e.g.: ::

    from cfd_package.types import CFDPackage

    class AnotherServer(YourServer):
        """
        This server subclasses the other server and will already have the file declared above, in addition to
        any types declared in this class.
        """
        modules = [
            CFDPackage("nginx"),
        ]

This class of servers will now both have the file /etc/motd and the package nginx installed. To match this class
with a specific server, you have to register it in the ``node_registry``. This is done the following way: ::

    from cfd.pool import node_registry
    node_registry.register(AnotherServer, 'server-1.organization.org')

Make sure the ``cfd-server`` is running and then you are ready to run the cfd agent on ``server-1.organization.org``::

    cfd-agent

You should receive ``Wrong credentials for server-1.organization.org``. You need to create create an api key for the
server and place it in /etc/cfd/config.yaml. ::

    $ cfd-server create-api-key server-1.organization.org
    xcxcxcxcxcxcxcxxcxc

``/etc/cfd/conf.yaml``: ::

    ---
        api-key: xcxcxcxcxcxcxcxxcxc

Now run ``cfd-agent`` again and it should add the package and the file.

An important part of CFD is the ability to write plugable modules that can be shared with everyone else. Lets create
a small module to handle our MOTD file. ::

    from cfd.modules import CFDModule
    from cfd.types import CFDFile


    class MOTD(CFDModule):
        def __init__(self, content):
            self.add(CFDFile("", content=content))

While this is obviously a very simple example, you can customize the __init__ method to accept whatever argument you
want, such as providing all the possible configurations for a software and generating configuration files depending
on it. The module can then be imported and added to the module list on the node. ::

    class SomeNode(CFDNode):
        modules = [
            MOTD('hello'),
        ]

Congrats, you're done!