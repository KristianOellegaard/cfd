from cfd.functions import CFDFile
from cfd.nodes import CFDNode
from cfd.pool import node_registry
from cfd_nginx.module import NginxServer, NginxVirtualHost


class WebServer(CFDNode):
    modules = [
        NginxServer(worker_processes=2),
    ]


class SpecificWebServer(WebServer):
    @property
    def modules(self):
        return [
            NginxVirtualHost(self.facts.get('hostname'))
        ]


for server_id in range(1, 10):
    node_registry.register(SpecificWebServer, 'server-%s.organization.org' % server_id)