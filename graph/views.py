from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json
import uuid

from accounts.models import Account
from accounts.views import login
import graph.ols
import graph.graph
import datetime

def start(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))
		
	return render(request, 'start.html')
	
def workingWith(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))

	return HttpResponse(json.dumps(graph.ols.workingWith(user), sort_keys=True, indent=4))

def trendingAround(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))

	return HttpResponse(json.dumps(graph.ols.trendingAround(user), sort_keys=True, indent=4))

def people(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))
		
	return HttpResponse('<pre>' + json.dumps(graph.ols.get_relationships(user), sort_keys=True, indent=4) + '</pre>')

def calendar(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))
	
	return HttpResponse("<pre>" + json.dumps(graph.graph.get_my_calendar(user), sort_keys=True, indent=4) + "</pre>")
	
def my_files(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))

	files_last_edited_by_others = []
	files = graph.graph.get_my_files(user)

	for file in files['value']:
		if "id" in file['lastModifiedBy']['user'] and uuid.UUID(file['lastModifiedBy']['user']['id']) != user.id:
			files_last_edited_by_others.append(file)

	return HttpResponse(json.dumps(files_last_edited_by_others, sort_keys=True, indent=4))
	
def emails(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))
	
	return HttpResponse(json.dumps(graph.graph.get_my_emails(user), sort_keys=True, indent=4))

def trending_files(request):
	user = Account.login(request)
	if not user:
		return HttpResponseRedirect(reverse(login))
	
	return HttpResponse('<pre>' + json.dumps(graph.ols.get_trending_files(user), sort_keys = True, indent=4) + '</pre>')
