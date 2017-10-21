from django import forms
from .models import Recipe
from .models import Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'desc', 'duration', 'people', 'level',)
        labels = {
            "title": "Tittel",
            "desc": "Beskrivelse",
            "duration": "Tid",
            "people": "Antal personer",
            "level": "Vanskelighetsgrad",
        }
        help_texts = {
            "duration": "I hele minutter",
        }
        
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('title', 'amount', 'recipe')
