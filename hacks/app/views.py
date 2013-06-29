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
import os
import soundcloud
from hacks.settings import MEDIA_ROOT



@login_required
def add_song(request, circle_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            client = soundcloud.Client(
                access_token=request.session.get('access_token'))
            ext = os.path.splitext(file.name)[1]
            desc = '%s/tmp%s'%(MEDIA_ROOT, ext)
            destination = open(desc, 'wb')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
            track = client.post('/tracks', track={
                'title': form.cleaned_data['title'],
                'asset_data': open(desc, 'rb')
            })
            c = get_object_or_404(Circle, pk=circle_id)
            song = Song.objects.create (
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                url=track.permalink_url,
                circle=c,
                genre=form.cleaned_data['genre'])
            song.save()
            print track.permalink_url
            return HttpResponseRedirect('/class')
    return HttpResponseNotFound('No page')


@login_required
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
    return render_to_response('create_circle.html',{'form': form})

def home(request):
    return render_to_response('index.html', RequestContext(request))

def record(request):
    return render_to_response('record.html', RequestContext(request))

@require_http_methods(["POST"])
def action(request):
    return HttpResponse("Success")

def login(request):
    client = soundcloud.Client(client_id='0a12c93543fbf8de3cba545b5c16bd64',
                             client_secret='5dcac4b7f8d57485150f829a25104028',
                             redirect_uri='http://127.0.0.1:8000/redirect/')
    return redirect(client.authorize_url())

def private(request):
    client = soundcloud.Client(client_id='0a12c93543fbf8de3cba545b5c16bd64',
                            client_secret='5dcac4b7f8d57485150f829a25104028',
                            redirect_uri='http://127.0.0.1:8000/redirect/')
    code = request.GET['code']
    access_token = client.exchange_token(code)
    #client_user = soundcloud.Client(access_token=access_token)
    print "got here"
    current_user = client.get('/me')
    request.session['access_token'] = access_token.access_token
    if User.objects.filter(username=current_user.username):
        user = User.objects.get(username=current_user.username)
        user_auth = auth.authenticate(username=user.username, password='pwd')
        auth.login(request, user_auth)
    else:
        user = User(username=current_user.username)
        user.set_password('pwd')
        user.save()
        user_auth = auth.authenticate(username=user.username, password='pwd')
        auth.login(request, user_auth)
    return HttpResponseRedirect('/')

