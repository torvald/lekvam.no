from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.recipes, name='recipes'),
    url(r'^create$', views.create_recipe, name='create_recipe'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe'),
    url(r'^(?P<recipe_id>[0-9]+)/ingredients$', views.recipe_ingredients, name='recipe-ingredients'),
]
