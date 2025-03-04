
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SubscriptionTier(models.Model):
    """Defines subscription tiers for the app"""
    TIER_CHOICES = [
        ('basic', 'Basic - $5/month'),
        ('premium', 'Premium - $10/month')
    ]
    
    name = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.JSONField(default=dict)
    
    def __str__(self):
        return self.get_name_display()

class UserSubscription(models.Model):
    """Tracks user subscriptions"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def is_valid(self):
        return self.is_active and (self.end_date is None or self.end_date > timezone.now())

class AdReward(models.Model):
    """Tracks ad-based rewards for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_type = models.CharField(max_length=50)  # e.g., 'meal_plan', 'recipe'
    reward_date = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

class ReferralProgram(models.Model):
    """Tracks user referrals and rewards"""
    referrer = models.ForeignKey(User, related_name='referrals_made', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referral_used', on_delete=models.CASCADE)
    reward_tier = models.ForeignKey(SubscriptionTier, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_rewarded = models.BooleanField(default=False)
