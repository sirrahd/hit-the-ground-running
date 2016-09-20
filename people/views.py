from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json

from accounts.models import Account
from people.helpers import get_new_connections

def connections(request):
    user = Account.login(request)
    if not user:
        return HttpResponseRedirect(reverse(login))

    get_new_connections(user)

    connections = []
    for c in user.people.all():
        connections.append(c.dict())

    return HttpResponse('<pre>' + json.dumps(connections) + '</pre>')