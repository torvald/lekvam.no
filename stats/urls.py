from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.stats, name='stats'),
    url(r'^gauge/(?P<slug>[a-z0-9\-]+)/add$', views.gauge_add, name='gauge-add'),
]
