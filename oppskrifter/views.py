from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Recipe
from .models import Step
from .models import Ingredient
from .forms import RecipeForm
from .forms import StepForm
from .forms import IngredientForm

from django.http import JsonResponse
from django.template.loader import render_to_string

import datetime


def paginate(request, objects_list):
    paginator = Paginator(objects_list, 3)

    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)
    return objects


##### List of recipes #####

def recipes(request):
    recipes = Recipe.objects.filter(deleted__isnull = True)
    recipes = paginate(request, recipes)
    return render(request, 'recipes.html', {'recipes': recipes})


####### recipe stuff #######


# Get one recipe, include logical blocks
def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

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
    recipe.deleted = datetime.datetime.now()
    recipe.save()
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
        error = _save_ingredient(request, recipe)
        if error:
            context['error'] = error
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
    else:
        return form.errors


####### step stufff ##########

@login_required
def ajax_recipe_steps(request, recipe_id):
    """
    Only called by ajax
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return HttpResponse(_recipe_steps(request, recipe))

@login_required
def delete_step(request, recipe_id, step_id):
    step = get_object_or_404(Step, id=step_id)
    _only_allow_owner(request, step)
    step.delete()
    # ajax call from steplist, return the list
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return HttpResponse(_recipe_steps(request, recipe))

def _recipe_steps(request, recipe):
    context = {'user': request.user,
               'recipe': recipe}
    if request.method == 'POST':
        _only_allow_owner(request, recipe)
        error =_save_step(request, recipe)
        if error:
            context['error'] = error
    steps = Step.objects.filter(recipe_id=recipe.id).order_by('id')
    context['steps'] = _sort_steps_and_add_numbers(steps)
    return render_to_string('recipe_steps.html', context)

def _save_step(request, recipe):
    """
    Logic for saving steps, ACL in parent function
    """
    post = request.POST
    files = request.FILES
    post._mutable = True
    post['recipe'] = recipe.id

    form = StepForm(post, files)
    if form.is_valid():
        step = form.save()
    else:
        return form.errors

def _sort_steps_and_add_numbers(steps):
    tagged_list = []
    counter = 0
    for step in steps:
        counter = counter + 1
        weight = counter + step.weight
        tagged_list.append((counter, step, weight))
        # TODO

    print tagged_list
    return tagged_list

####### stuff #######

def _only_allow_owner(request, obj):
    if request.user.id != obj.owner.id:
        raise PermissionDenied
        #return HttpResponseForbidden()
