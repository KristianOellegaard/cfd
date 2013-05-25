from cfd.types import CFDFile, CFDDebug
from cfd.nodes import CFDNode
from cfd.pool import node_registry
from cfd_nginx.module import NginxServer, NginxVirtualHost
from cfd_package.types import CFDPackage


class WebServer(CFDNode):
    modules = [
        NginxServer(worker_processes=2),
    ]


class CFDServer(WebServer):
    modules = [
        CFDDebug("hello"),
        CFDFile("/etc/motd", content="hello from CFD"),
    ]

node_registry.register(CFDServer, 'cfd.testorg.org')


class SpecificWebServer(WebServer):
    @property
    def modules(self):
        return [
            NginxVirtualHost(self.facts.get('hostname')),
            CFDPackage('zach', package_manager='pip', version='1.1', ensure=False),
            CFDPackage('python-cloudfoundry', package_manager='pip', version='0.2', ensure=True)
        ]


for server_id in range(1, 10):
    node_registry.register(SpecificWebServer, 'server-%s.organization.org' % server_id)