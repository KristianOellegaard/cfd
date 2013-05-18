import json
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from cfd.models import Server, ApiKey, Fact
from cfd.pool import node_registry

@csrf_exempt
def host(request, hostname):
    facts = request.POST.copy()
    try:
        api_key = request.META.get("HTTP_APIKEY")
    except KeyError:
        return HttpResponseForbidden("No credentials provided")
    server, created = Server.objects.get_or_create(hostname=hostname)
    if ApiKey.objects.filter(server=server, api_key=api_key, active=True).exists():
        try:
            data = node_registry[hostname](hostname, facts).as_dict()
        except KeyError:
            raise Http404("Host not registered in definitions.py")
        for name, value in facts.items():
            fact, created = Fact.objects.get_or_create(server=server, name=name)
            fact.value = value
            fact.save()
    else:
        return HttpResponseForbidden("Wrong credentials for %s" % server.hostname)
    return HttpResponse(json.dumps(data))