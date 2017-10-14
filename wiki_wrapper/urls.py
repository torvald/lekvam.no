from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<slug>.*)$', views.node, name='wiki_node'),
]
