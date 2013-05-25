#!/usr/bin/env python
import os
import sys


def run():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfd_example.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    run()
