from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from .models import Recipe
from .models import Ingredient
from .forms import RecipeForm
from .forms import IngredientForm

from django.http import JsonResponse
from django.template.loader import render_to_string


# List of recipes
def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})


####### recipe stuff #######


# Get one recipe, include logical blocks
def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    ingredients = _recipe_ingredients(request, recipe_id)
    div = {'ingredients': ingredients}

    return render(request, 'recipe.html', {'recipe': recipe,
                                           'div': div})

def create_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        return _save_recipe(request, form)
    context = {'form': form}
    return render(request, 'recipe_form.html', context)


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if request.method == 'POST':
        return _save_recipe(request, form)
    context = {'form': form}
    return render(request, 'recipe_form.html', context)

def delete_recipe(request, recipe_id):
    """
    Call from delete button on recipe page. Deletes recipe and returns to list
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('recipes')

def _save_recipe(request, form):
    """
    Gets called by create_recipe and edit_recipe when method is POST
    """
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.owner = request.user
        recipe.save()
        return redirect('recipe', recipe_id=recipe.pk)
    else:
        context = {'form': form, 'error': "Feil"}
        return render(request, 'recipe_form.html', context)

####### ingredient stuff #######

def ajax_recipe_ingredients(request, recipe_id):
    """
    Only called by ajax
    """
    return HttpResponse(_recipe_ingredients(request, recipe_id))

def delete_ingredient(request, recipe_id, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    ingredient.delete()
    # ajax call from ingredientlist, return the list
    return HttpResponse(_recipe_ingredients(request, recipe_id))

def _recipe_ingredients(request, recipe_id):
    context = {}
    if request.method == 'POST':
        _save_ingredient(request, recipe_id) 
    context['ingredients'] = Ingredient.objects.filter(recipe_id=recipe_id)
    return render_to_string('recipe_ingredients.html', context)

def _save_ingredient(request, recipe_id):
    """
    Gets called by create_recipe and edit_recipe when method is POST
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    post = request.POST
    post._mutable = True
    post['recipe'] = recipe_id

    form = IngredientForm(post)
    if form.is_valid():
        ingredient = form.save()
    else:
        return False


####### stuff #######


def permission_denied(request):
    return HttpResponseForbidden()
    # return render(request, '403.html', {})
