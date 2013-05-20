# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.

import os
import sys

from gunicorn import util
from gunicorn.app.base import Application


class WSGIApplication(Application):

    def init(self, parser, opts, args):
        self.cfg.set("default_proc_name", "cfd-server")
        self.app_uri = "cfd_server.wsgi:application"

        sys.path.insert(0, os.getcwd())

    def load(self):
        return util.import_app(self.app_uri)


def run():
    """\
    The ``gunicorn`` command line runner for launching Gunicorn with
    generic WSGI applications.
    """
    WSGIApplication("%(prog)s [OPTIONS] APP_MODULE").run()