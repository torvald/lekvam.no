from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


# Create your models here.

class Recipe(models.Model):
    EASY = 1
    MODERATE = 2
    HARD = 3
    LEVELS = (
        (EASY, 'Lett'),
        (MODERATE, 'Moderat'),
        (HARD, 'Vanskelig'),
    )

    title = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.PositiveIntegerField()
    people = models.PositiveIntegerField(validators=[MaxValueValidator(20),MinValueValidator(1)])
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    deleted = models.DateTimeField(null=True, blank=True)

    image = models.FileField(upload_to='images/', null=True, blank=True)

    @property
    def sub_recipes_caption(self):
        # TODO
        return ""

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_formatted(self):
        amount = str(self.amount)
        return amount.rstrip('0').rstrip('.') if '.' in amount else amount

    @property
    def owner(self):
        return self.recipe.owner

    def __str__(self):
        return str(self.amount) + " " + self.title


class Rate(models.Model):
    rater = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    weight = models.IntegerField()

    @property
    def owner(self):
        return self.recipe.owner
