"""hack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import graph.views
import accounts.views
import people.views

urlpatterns = [
    url(r'^$', graph.views.start, name='start'),
    url(r'^people/$', graph.views.people, name='people'),
    url(r'^trending_files/$', graph.views.trending_files, name='trending_files'),
	url(r'^my_files/$', graph.views.my_files, name='my_files'),
	url(r'^calendar/$', graph.views.calendar, name='calendar'),
	url(r'^emails/$', graph.views.emails, name='emails'),
	url(r'^workingWith/$', graph.views.workingWith, name='workingWith'),
	url(r'^trendingAround/$', graph.views.trendingAround, name='trendingAround'),

    url(r'^login/$', accounts.views.login, name='login'),
    url(r'^logout/$', accounts.views.logout, name='logout'),
    url(r'^reset/$', accounts.views.reset, name='reset'),
    url(r'^auth/$', accounts.views.auth, name='auth'),
    url(r'^gettoken/$', accounts.views.gettoken, name='gettoken'),

    url(r'^connections/$', people.views.connections, name='connections'),
]
