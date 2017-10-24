from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pano$', views.pano, name='webcam_pano'),
    url(r'^pano/(?P<date>\d{4}-\d{2}-\d{2})$', views.pano, name='webcam_pano_date'),
    url(r'^live$', views.live, name='webcam_live'),
]
