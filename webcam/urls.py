from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='webcam_index'),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})$', views.index, name='webcam_index'),
]
