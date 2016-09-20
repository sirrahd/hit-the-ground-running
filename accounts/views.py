from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json

from accounts.models import Account
from people.helpers import get_new_connections
from files.helpers import get_new_files
import graph.auth

def login(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    
    user = Account.login(request, request.POST['email'], request.POST['password'])
    if not user:
        return HttpResponseRedirect(reverse(login))

    get_new_connections(user)
    get_new_files(user)

    return HttpResponseRedirect(reverse('auth'))

def logout(request):
    user = Account.login(request)
    if user:
        user.logout(request)
    
    return HttpResponseRedirect(reverse(login))

def reset(request):
    user = Account.login(request)
    if user:
        user.logout(request)
        user.delete()
    
    return HttpResponseRedirect(reverse(login))
    
def auth(request):
    user = Account.login(request)
    if not user:
        return HttpResponseRedirect(reverse(login))

    redirect_uri = request.build_absolute_uri(reverse('gettoken'))
    sign_in_url = graph.auth.get_signin_url(redirect_uri)
    return HttpResponseRedirect(sign_in_url)

def gettoken(request):
    user = Account.login(request)
    if not user:
        return HttpResponseRedirect(reverse(login))

    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('gettoken'))
    access_token = graph.auth.get_token_from_code(auth_code, redirect_uri)
    user.graph_token = access_token
    user.save()
    return HttpResponseRedirect(reverse('start'))