from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
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

# Get one recipe, include logical blocks
def recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    ingredients = _recipe_ingredients(request, recipe_id)
    div = {'ingredients': ingredients}

    return render(request, 'recipe.html', {'recipe': recipe,
                                           'div': div})
# Create a new recepi
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


def delete_recipe(request, recipe_id):
    """
    Call from delete button on recipe page. Deletes recipe and returns to list
    """
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect('recipes')


def delete_ingredient(request, recipe_id, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    ingredient.delete()
    # ajax call from ingredientlist, return the list
    return HttpResponse(_recipe_ingredients(request, recipe_id))

# AJAX endpoint, need http encapsulation
def recipe_ingredients(request, recipe_id):
    return HttpResponse(_recipe_ingredients(request, recipe_id))

# AJAX block logic
# all functions return string

def _recipe_ingredients(request, recipe_id):
    context = {}
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
    return render_to_string('recipe_ingredients.html', context)
