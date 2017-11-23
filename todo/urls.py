from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.todo, name='todo'),
    url(r'^notes$', views.ajax_add_note, name='add-note'),
#    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe'),
#    url(r'^(?P<recipe_id>[0-9]+)/edit$', views.edit_recipe, name='edit-recipe'),
    url(r'^notes/(?P<note_id>[0-9]+)$', views.ajax_edit_note, name='edit-note'),
    url(r'^notes/(?P<note_id>[0-9]+)/done$', views.ajax_mark_as_done, name='mark-as-done'),
    url(r'^notes/(?P<note_id>[0-9]+)/move$', views.ajax_move_note, name='move-note'),
#    url(r'^(?P<recipe_id>[0-9]+)/ingredients$', views.ajax_recipe_ingredients, name='recipe-ingredients'),
#    url(r'^(?P<recipe_id>[0-9]+)/ingredient/(?P<ingredient_id>[0-9]+)/delete$', views.delete_ingredient, name='recipe-delete-ingredient'),
#    url(r'^(?P<recipe_id>[0-9]+)/steps$', views.ajax_recipe_steps, name='recipe-steps'),
#    url(r'^(?P<recipe_id>[0-9]+)/step/(?P<step_id>[0-9]+)/delete$', views.delete_step, name='recipe-delete-step'),
#    url(r'^(?P<recipe_id>[0-9]+)/step/(?P<step_id>[0-9]+)/move/(?P<direction>(up|down))$', views.move_step, name='recipe-move-step'),
]
