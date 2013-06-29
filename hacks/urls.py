from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'hacks.app.views.home'),
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^create_circle/$', 'hacks.app.views.create_circle'),
    url(r'^circle/(?P<circle_id>\d_/song/$', 'hacks.app.views.add_song'),
    url(r'^circle/(?P<circle_id>\d+)/$', 'hacks.app.views.circle'),
    # Examples:
    # url(r'^$', 'hacks.views.home', name='home'),
    # url(r'^hacks/', include('hacks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
