from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.stats, name='stats'),
    url(r'^gauge/(?P<slug>[a-z0-9\-]+)$', views.gauge_show, name='gauge-show'),
    url(r'^gauge/(?P<slug>[a-z0-9\-]+)/add$', views.gauge_add, name='gauge-add'),
    url(r'^event/(?P<slug>[a-z0-9\-]+)/add$', views.event_add, name='event-add'),
]
