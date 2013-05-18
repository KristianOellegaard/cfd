import json
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from cfd.pool import node_registry

@csrf_exempt
def host(request, hostname):
    facts = request.POST
    try:
        data = node_registry[hostname](hostname, facts).as_dict()
    except KeyError:
        raise Http404("Host does not exist")
    return HttpResponse(json.dumps(data))