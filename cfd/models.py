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
    api_key = models.CharField(max_length=32)
    date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField()
