from django.template import Context
from django.template.loader import render_to_string
from cfd.functions import CFDPackage, CFDFile
from cfd.modules import CFDModule


class NginxServer(CFDModule):
    def __init__(
            self,
            accept_mutex=None,
            accept_mutex_delay=None,
            daemon=None,
            debug_connection=None,
            debug_points=None,
            error_log=None,
            env=None,
            events=None,
            include=None,
            lock_file=None,
            master_process=None,
            multi_accept=None,
            pcre_jit=None,
            pid=None,
            ssl_engine=None,
            timer_resolution=None,
            use=None,
            user=None,
            worker_aio_requests=None,
            worker_connections=None,
            worker_cpu_affinity=None,
            worker_priority=None,
            worker_processes=None,
            worker_rlimit_core=None,
            worker_rlimit_nofile=None,
            worker_rlimit_sigpending=None,
            working_directory=None):
        super(NginxServer, self).__init__()
        self.accept_mutex = accept_mutex
        self.accept_mutex_delay = accept_mutex_delay
        self.daemon = daemon
        self.debug_connection = debug_connection
        self.debug_points = debug_points
        self.error_log = error_log
        self.env = env
        self.events = events
        self.include = include
        self.lock_file = lock_file
        self.master_process = master_process
        self.multi_accept = multi_accept
        self.pcre_jit = pcre_jit
        self.pid = pid
        self.ssl_engine = ssl_engine
        self.timer_resolution = timer_resolution
        self.use = use
        self.user = user
        self.worker_aio_requests = worker_aio_requests
        self.worker_connections = worker_connections
        self.worker_cpu_affinity = worker_cpu_affinity
        self.worker_priority = worker_priority
        self.worker_processes = worker_processes
        self.worker_rlimit_core = worker_rlimit_core
        self.worker_rlimit_nofile = worker_rlimit_nofile
        self.worker_rlimit_sigpending = worker_rlimit_sigpending
        self.working_directory = working_directory

        self.add(
            CFDPackage("nginx"),
            CFDFile(
                path="/etc/nginx/nginx.conf",
                ensure=True,
                content=render_to_string("cfd_nginx/nginx.conf", context_instance=Context({'nginx_server': self}))
            ),
        )


class NginxVirtualHost(CFDModule):
    def __init__(self, domain):
        super(NginxVirtualHost, self).__init__()

        self.add(
            CFDFile(path="/etc/nginx/sites-available/%s.conf" % domain, ensure=True, content="Hello!")
        )