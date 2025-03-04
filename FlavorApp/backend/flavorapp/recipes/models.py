from django.db import models
from django.conf import settings
from authentication.models import CustomUser

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}"

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    cooking_time = models.CharField(max_length=100)
    servings = models.CharField(max_length=50)
    nutritional_info = models.JSONField(default=dict)
    
    category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_ai_generated = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RecipeVote(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote_value = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe', 'user')

class MealPlan(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Recipe)
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class FlavorChallenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    challenge_recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title

class ChallengeBadge(models.Model):
    challenge = models.ForeignKey(FlavorChallenge, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge_type = models.CharField(max_length=50, choices=[
        ('winner', 'Challenge Winner'),
        ('participant', 'Challenge Participant')
    ])
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('challenge', 'user')
