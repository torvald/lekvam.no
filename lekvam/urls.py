from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'common.views.home', name='home'),
    url(r'^oppskrifter/', include('oppskrifter.urls')),
    url(r'^webcam/', include('webcam.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
