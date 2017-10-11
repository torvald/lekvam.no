from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Recipe
from .forms import RecipeForm

from django.http import JsonResponse
from django.template.loader import render_to_string


def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe.html', {'recipe': recipe})


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
