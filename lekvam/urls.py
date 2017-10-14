from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # Examples
    #url(r'^$', 'common.views.home', name='wiki_start'),
    url(r'^$', RedirectView.as_view(url='/wiki/start')),
    url(r'^wiki/', include('wiki_wrapper.urls')),
    url(r'^oppskrifter/', include('oppskrifter.urls')),
    url(r'^webcam/', include('webcam.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
