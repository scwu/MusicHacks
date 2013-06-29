from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.contrib.auth import *
from django import forms
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.db.models import Q
from hacks.app.models import *
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.core.context_processors import csrf

from datetime import datetime
import hacks.urls
import json

def home(request):
    return render_to_response('index.html',RequestContext(request))

def circle(request):
    return render_to_response('circle.html', RequestContext(request))
