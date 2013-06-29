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
from django.views.decorators.http import require_http_methods

from .forms import UploadFileForm

from datetime import datetime
import hacks.urls
import json

import soundcloud

def home(request):
    return render_to_response('index.html',RequestContext(request))

def add_song(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(Request.FILES['file'])
            return HttpResponseRedirect('/class')
    else:
        form = UploadFileForm()

    return render_to_response('add_song.html', {'form' : form})

def circle(request):
    return render_to_response('circle.html', RequestContext(request))

@require_http_methods(["POST"])
def action(request):
    return HttpResponse("Success")
