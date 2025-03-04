from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    total_flavor_points = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    
    # Social login fields
    google_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    facebook_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    # Subscription and payment related
    is_premium_user = models.BooleanField(default=False)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dietary_preferences = models.JSONField(default=dict)
    allergies = models.JSONField(default=list)
    cooking_skill_level = models.CharField(
        max_length=20, 
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
