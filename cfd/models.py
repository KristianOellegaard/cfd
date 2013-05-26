import hashlib
import random
from django.db import models
from django.utils import timezone


class Server(models.Model):
    hostname = models.CharField(max_length=256)


class Fact(models.Model):
    server = models.ForeignKey(Server)
    name = models.CharField(max_length=128)
    value = models.TextField()


class ApiKey(models.Model):
    server = models.ForeignKey(Server)
    api_key = models.CharField(max_length=56)
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField()

    @classmethod
    def create(cls, server):
        ApiKey.objects.filter(server=server, active=True).update(active=False)
        api_key = hashlib.sha224(str(random.getrandbits(256))).hexdigest()
        return ApiKey.objects.create(server=server, api_key=api_key, active=True)
