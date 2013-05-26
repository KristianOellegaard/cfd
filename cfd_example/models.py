from cfd.types import CFDFile, CFDDebug
from cfd.nodes import CFDNode
from cfd.pool import node_registry
from cfd_nginx.module import NginxServer, NginxVirtualHost
from cfd_package.types import CFDPackage


class CFDServer(CFDNode):
    def modules(self):
        return [
            CFDDebug("hello"),
            CFDFile("/etc/update-motd.d/cfd",
                    content="CFD Managed Server. This is %s" % self.facts.get('hostname'),
                    mode="755"),
        ]

node_registry.register(CFDServer, 'cfd.testorg.org')
node_registry.register(CFDServer, 'server-1.testorg.org')
