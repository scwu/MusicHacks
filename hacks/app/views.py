from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
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

from django.forms import ModelForm

from .forms import UploadFileForm

from datetime import datetime
import hacks.urls
import json

import soundcloud


@login_required
def add_song(request, circle_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            client = soundcloud.Client(
                access_token=request.session['access_token'])
            track = client.post('/tracks', track={
                'title': form.cleaned_data['title'],
                'asset_data': file
            })
            print track.permalink_url
            return HttpResponseRedirect('/class')
    return HttpResponseNotFound('No page')

def circle(request, circle_id):
    form = UploadFileForm()
    model = Circle.objects.get(pk=circle_id)

    return render_to_response(
        'add_song.html',
        {'form': form,
         'model': model},
        context_instance=RequestContext(request))

@login_required
def create_circle(request):
    class CircleForm(ModelForm):
        class Meta:
            model = Circle
            fields = ['users', 'title', 'teacher']
    if request.method == 'POST':
        form = CircleForm(request.POST)
        circle.save()
        return HttpResponseRedirect('/circle/%d' % (circle.id))
    else:
        form = CircleForm()
    return render_to_response('create_circle.html')

def home(request):
    return render_to_response('circle.html', RequestContext(request))


@require_http_methods(["POST"])
def action(request):
    return HttpResponse("Success")
