from django.db import models

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
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.IntegerField()
    people = models.IntegerField()
    level = models.PositiveSmallIntegerField(choices=LEVELS)
    deleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        amount = str(self.amount)
        amount = amount.rstrip('0').rstrip('.') if '.' in amount else amount
        return amount + " " + self.title

class Rate(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField()

