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
import urllib2


@login_required
def add_song(request, circle_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        client = soundcloud.Client(
            access_token=request.session.get('access_token'))
        ext = os.path.splitext(file.name)[1]
        desc = '%s/tmp%s'%(MEDIA_ROOT, ext)
        destination = open(desc, 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        t = open(desc, 'rb')
        track = {
            'title': 'Sample song',
            'asset_data': t
        }
        track = client.post('/tracks', track=track)
        c = get_object_or_404(Circle, pk=circle_id)
        song = Song.objects.create (
            user=request.user,
            title='Sample song',
            description='',
            url=track.uri,
            circle=c)
        song.save()
        return HttpResponseRedirect('/circle/%s' % circle_id)
    return HttpResponseNotFound('No page')


@login_required
def circle(request, circle_id):
    form = UploadFileForm()
    link = Circle.objects.get(pk=circle_id)
    songs = Song.objects.filter(circle=link).values()
    insp =  Inspiration.objects.filter(circle=link)
    youtube = []
    wiki = []
    spotify = []
    for i in insp:
        if "youtube" in i.url:
            iy = { "url" : i.url, "title" : i.title}
            youtube.append(iy)
        elif "wikipedia" in i.url:
            wi = { "url" : i.url, "title" : i.title }
            wiki.append(wi)
        else:
            si = { "url" : i.url, "title" : i.title }
            spotify.append(si)

    return render_to_response(
        'circle.html',
        {'form': form,
         'songs': songs,
         'image' : link.background_image,
         'title' : link.title,
         'description' : link.description,
         'youtube' : youtube,
         'wikipedia' : wiki,
         'spotify' : spotify,
         },
        context_instance=RequestContext(request))

@login_required
def create_circle(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        background_img = request.POST['background_image']
        due_date = request.POST['due_date']
        youtube = request.POST['youtube']
        youtube_title = request.POST['youtube_title']
        wikipedia = request.POST['wiki']
        wiki_title = request.POST['wiki_title']
        spotify = request.POST['spotify']
        spotify_title = request.POST['spotify_title']
        date_time = datetime.strptime(due_date, '%I:%M%p')
        teacher = User.objects.get(username=request.user.username)
        c = Circle(title=title, description=description,
                   background_image = background_img,
                   due_date=date_time, teacher=teacher)
        c.save()
        yt = Inspiration(circle=c, url=youtube, title=youtube_title)
        yt.save()
        wikit = Inspiration(circle=c, url=wikipedia, title=wiki_title)
        wikit.save()
        st = Inspiration(circle=c, url=spotify, title=spotify_title)
        st.save()
        return HttpResponseRedirect('/circle/%d' % (c.id))
    else:
        return render_to_response('create_circle.html')

def home(request):
    circles = Circle.objects.all().values()
    return render_to_response('index.html', {'circles':circles}, RequestContext(request))

# temporary routes
def jeremy(request):
    return render_to_response('circle.html', RequestContext(request))

def record(request):
    return render_to_response('record.html', RequestContext(request))

@login_required
def join_circle(request, circle_id):
    c = get_object_or_404(Circle, pk=circle_id)
    user = User.objects.get(username=request.user.username)
    c.users.add(user)
    c.save()
    return HttpResponseRedirect('/circle/%s' % (circle_id))

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
