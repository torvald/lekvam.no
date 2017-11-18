from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.todo, name='todo'),
#    url(r'^create$', views.create_recipe, name='create_recipe'),
#    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe'),
#    url(r'^(?P<recipe_id>[0-9]+)/edit$', views.edit_recipe, name='edit-recipe'),
#    url(r'^(?P<recipe_id>[0-9]+)/delete$', views.delete_recipe, name='delete-recipe'),
#    url(r'^(?P<recipe_id>[0-9]+)/ingredients$', views.ajax_recipe_ingredients, name='recipe-ingredients'),
#    url(r'^(?P<recipe_id>[0-9]+)/ingredient/(?P<ingredient_id>[0-9]+)/delete$', views.delete_ingredient, name='recipe-delete-ingredient'),
#    url(r'^(?P<recipe_id>[0-9]+)/steps$', views.ajax_recipe_steps, name='recipe-steps'),
#    url(r'^(?P<recipe_id>[0-9]+)/step/(?P<step_id>[0-9]+)/delete$', views.delete_step, name='recipe-delete-step'),
#    url(r'^(?P<recipe_id>[0-9]+)/step/(?P<step_id>[0-9]+)/move/(?P<direction>(up|down))$', views.move_step, name='recipe-move-step'),
]
