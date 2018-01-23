from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples
    #url(r'^$', 'common.views.home', name='wiki_start'),
    url(r'^$', RedirectView.as_view(url='/wiki/start')),
    url(r'^wiki/', include('wiki_wrapper.urls')),
    url(r'^oppskrifter/', include('oppskrifter.urls')),
    url(r'^webcam/', include('webcam.urls')),
    url(r'^todo/', include('todo.urls')),
    url(r'^stats/', include('stats.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
)
