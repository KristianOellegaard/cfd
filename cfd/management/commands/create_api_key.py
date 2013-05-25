from django.core.management.base import BaseCommand, CommandError
from cfd.models import ApiKey, Server


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            hostname = args[0]
        except IndexError:
            print "Please provider a hostname as first argument"
            exit(1)
            return
        server, created = Server.objects.get_or_create(hostname=hostname)
        api_key = ApiKey.create(server)
        print api_key.api_key
