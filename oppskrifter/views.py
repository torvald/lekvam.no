from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Recipe
from .models import Ingredient
from .forms import RecipeForm
from .forms import IngredientForm

from django.http import JsonResponse
from django.template.loader import render_to_string


def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    ingredients = render_to_string('recipe_ingredients.html', None, None)
    div = {'ingredients': ingredients}

    return render(request, 'recipe.html', {'recipe': recipe,
                                           'div': div})

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe', recipe_id=recipe.id)
        else:
            context = {'form': form, 'error': "Feil"}
            return render(request, 'recipe_form.html', context)
    
    form = RecipeForm()
    context = {'form': form}
    return render(request, 'recipe_form.html', context)

def recipe_ingredients(request, recipe_id):
    context = {}
    if request.method == 'DELETE':
       pass
    if request.method == 'POST':
        post = request.POST
        post._mutable = True
        post['recipe'] = recipe_id
        
        form = IngredientForm(post)
        if form.is_valid():
            ingredient = form.save()
        else:
            context['error'] = "Feil i skjema"
   
    context['ingredients'] = Ingredient.objects.filter(recipe_id=recipe_id)
    return render(request, 'recipe_ingredients.html', context)
