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


##### List of recipes #####


def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})


####### recipe stuff #######


# Get one recipe, include logical blocks
def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    #user = request.user if request.user.is_auth

    ingredients = _recipe_ingredients(request, recipe)
    steps       = _recipe_steps(request, recipe)
    div = {'ingredients': ingredients,
           'steps': steps}

    return render(request, 'recipe.html', {'recipe': recipe,
                                           'user': request.user,
                                           'div': div})

@login_required
def create_recipe(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        return _save_recipe(request, form)
    context = {'form': form}
    return render(request, 'recipe_form.html', context)


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if request.method == 'POST':
        _only_allow_owner(request, recipe)
        return _save_recipe(request, form)
    context = {'form': form}
    return render(request, 'recipe_form.html', context)

@login_required
def delete_recipe(request, recipe_id):
    """
    Call from delete button on recipe page. Deletes recipe and returns to list
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _only_allow_owner(request, recipe)
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

@login_required
def ajax_recipe_ingredients(request, recipe_id):
    """
    Only called by ajax
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return HttpResponse(_recipe_ingredients(request, recipe))

@login_required
def delete_ingredient(request, recipe_id, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    _only_allow_owner(request, ingredient)
    ingredient.delete()
    # ajax call from ingredientlist, return the list
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return HttpResponse(_recipe_ingredients(request, recipe))

def _recipe_ingredients(request, recipe):
    context = {'user': request.user,
               'recipe': recipe}
    if request.method == 'POST':
        _only_allow_owner(request, recipe)
        _save_ingredient(request, recipe) 
    context['ingredients'] = Ingredient.objects.filter(recipe_id=recipe.id)
    return render_to_string('recipe_ingredients.html', context)

def _save_ingredient(request, recipe):
    """
    Logic for saving ingredients, ACL in parent function
    """
    post = request.POST
    post._mutable = True
    post['recipe'] = recipe.id

    form = IngredientForm(post)
    if form.is_valid():
        ingredient = form.save()


####### step stufff ##########

def _recipe_steps(request, recipe):
    context = {'user': request.user,
               'recipe': recipe}
    #if request.method == 'POST':
    #    _save_ingredient(request, recipe_id)
    #context['ingredients'] = Ingredient.objects.filter(recipe_id=recipe_id)
    return render_to_string('recipe_steps.html', context)

####### stuff #######

def _only_allow_owner(request, obj):
    if request.user.id != obj.owner.id:
        raise PermissionDenied
        #return HttpResponseForbidden()
