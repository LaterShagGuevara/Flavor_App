import os
import sys
import json
import subprocess

class FlavorAppMonetizationSetup:
    def __init__(self):
        self.project_root = r'c:\Users\sbrea\Desktop\FlavorApp'
        self.backend_dir = os.path.join(self.project_root, 'backend')
        self.frontend_dir = os.path.join(self.project_root, 'frontend')
        self.env_name = 'flavorapp_env'

    def run_command(self, command, cwd=None, shell=True, capture_output=True):
        """Run a shell command and handle output."""
        try:
            result = subprocess.run(
                command, 
                cwd=cwd, 
                shell=shell, 
                capture_output=capture_output, 
                text=True
            )
            print(f"Command: {command}")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return result
        except Exception as e:
            print(f"Error running command: {e}")
            return None

    def create_monetization_models(self):
        """Create Django models for monetization features"""
        monetization_models_path = os.path.join(
            self.backend_dir, 
            'flavorapp', 
            'monetization', 
            'models.py'
        )
        os.makedirs(os.path.dirname(monetization_models_path), exist_ok=True)
        
        models_content = '''
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
'''
        with open(monetization_models_path, 'w') as f:
            f.write(models_content)

    def create_monetization_services(self):
        """Create services for handling monetization logic"""
        monetization_services_path = os.path.join(
            self.backend_dir, 
            'flavorapp', 
            'monetization', 
            'services.py'
        )
        
        services_content = '''
import stripe
from django.conf import settings
from .models import SubscriptionTier, UserSubscription, AdReward, ReferralProgram

class PaymentService:
    """Handles payment processing via Stripe"""
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_subscription(self, user, tier_name):
        """Create a Stripe subscription for a user"""
        tier = SubscriptionTier.objects.get(name=tier_name)
        
        # Create Stripe customer if not exists
        customer = stripe.Customer.create(
            email=user.email,
            source=None  # You'd typically get this from frontend
        )
        
        # Create Stripe subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{tier.get_name_display()} Subscription',
                    },
                    'unit_amount': int(tier.price * 100),
                    'recurring': {'interval': 'month'}
                }
            }]
        )
        
        # Create local subscription record
        UserSubscription.objects.create(
            user=user,
            tier=tier,
            is_active=True
        )
        
        return subscription

class AdService:
    """Manages ad-based rewards and interactions"""
    def award_ad_reward(self, user, ad_type):
        """Award user for watching an ad"""
        reward = AdReward.objects.create(
            user=user,
            ad_type=ad_type,
            expires_at=timezone.now() + timezone.timedelta(days=1)
        )
        return reward

class ReferralService:
    """Manages referral program logic"""
    def process_referral(self, referrer, referred_user):
        """Process a successful referral"""
        # Determine reward tier based on referred user's first subscription
        reward_tier = SubscriptionTier.objects.get(name='basic')
        
        referral = ReferralProgram.objects.create(
            referrer=referrer,
            referred_user=referred_user,
            reward_tier=reward_tier,
            is_rewarded=False
        )
        
        return referral
'''
        with open(monetization_services_path, 'w') as f:
            f.write(services_content)

    def update_backend_settings(self):
        """Update Django settings to include monetization configurations"""
        settings_path = os.path.join(
            self.backend_dir, 
            'flavorapp', 
            'settings.py'
        )
        
        # Create settings file if it doesn't exist
        if not os.path.exists(settings_path):
            default_settings_content = '''
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flavorapp.monetization',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
            with open(settings_path, 'w') as f:
                f.write(default_settings_content)
        
        # Read existing settings
        with open(settings_path, 'r') as f:
            settings_content = f.read()
        
        # Add monetization-related settings
        monetization_settings = '''
# Monetization Settings
STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
STRIPE_SECRET_KEY = 'your_stripe_secret_key'

ADMOB_APP_ID = 'ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy'
FACEBOOK_AD_ID = 'your_facebook_ad_id'

# Subscription Tiers
SUBSCRIPTION_TIERS = {
    'basic': {
        'price': 5.00,
        'features': ['remove_ads', 'meal_planning', 'grocery_list']
    },
    'premium': {
        'price': 10.00,
        'features': ['full_customization', 'exclusive_recipes']
    }
}

# Referral Program Settings
REFERRAL_REWARDS = {
    'basic_tier_days': 14,
    'premium_tier_days': 7
}
'''
        
        # Append to settings
        with open(settings_path, 'a') as f:
            f.write(monetization_settings)

    def update_frontend_monetization(self):
        """Update frontend to include monetization components"""
        # Web Frontend
        web_monetization_service = os.path.join(
            self.frontend_dir, 'web', 'src', 'services', 'MonetizationService.ts'
        )
        
        web_service_content = '''
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';

class MonetizationService {
    private stripePromise = loadStripe('your_stripe_public_key');

    async createSubscription(tier: 'basic' | 'premium') {
        try {
            const response = await axios.post('/api/subscriptions/create', { tier });
            const stripe = await this.stripePromise;
            
            // Redirect to Stripe Checkout
            const { error } = await stripe.redirectToCheckout({
                sessionId: response.data.sessionId
            });

            if (error) {
                console.error('Stripe Checkout Error:', error);
            }
        } catch (error) {
            console.error('Subscription Error:', error);
        }
    }

    async watchAdForReward(adType: string) {
        try {
            const response = await axios.post('/api/ads/reward', { adType });
            return response.data;
        } catch (error) {
            console.error('Ad Reward Error:', error);
        }
    }

    async processReferral(referredUserId: string) {
        try {
            const response = await axios.post('/api/referrals/process', { referredUserId });
            return response.data;
        } catch (error) {
            console.error('Referral Error:', error);
        }
    }
}

export default new MonetizationService();
'''
        os.makedirs(os.path.dirname(web_monetization_service), exist_ok=True)
        with open(web_monetization_service, 'w') as f:
            f.write(web_service_content)

        # Mobile Frontend (React Native)
        mobile_monetization_service = os.path.join(
            self.frontend_dir, 'mobile', 'src', 'services', 'MonetizationService.ts'
        )
        
        mobile_service_content = '''
import axios from 'axios';
import * as Stripe from 'expo-stripe-checkout';
import { AdMobInterstitial } from 'expo-ads-admob';

class MonetizationService {
    async createSubscription(tier: 'basic' | 'premium') {
        try {
            const response = await axios.post('/api/subscriptions/create', { tier });
            
            // Use Expo Stripe Checkout
            const { paymentIntent, error } = await Stripe.presentPaymentSheet({
                paymentIntentClientSecret: response.data.clientSecret
            });

            if (error) {
                console.error('Payment Error:', error);
            }
        } catch (error) {
            console.error('Subscription Error:', error);
        }
    }

    async showInterstitialAd() {
        try {
            // Configure AdMob Interstitial
            AdMobInterstitial.setAdUnitID('ca-app-pub-xxxxxxxxxxxxxxxx/yyyyyyyyyy');
            await AdMobInterstitial.requestAdAsync();
            await AdMobInterstitial.showAdAsync();
        } catch (error) {
            console.error('Ad Display Error:', error);
        }
    }

    async watchAdForReward(adType: string) {
        try {
            await this.showInterstitialAd();
            const response = await axios.post('/api/ads/reward', { adType });
            return response.data;
        } catch (error) {
            console.error('Ad Reward Error:', error);
        }
    }
}

export default new MonetizationService();
'''
        os.makedirs(os.path.dirname(mobile_monetization_service), exist_ok=True)
        with open(mobile_monetization_service, 'w') as f:
            f.write(mobile_service_content)

    def main(self):
        """Execute monetization setup"""
        print("Starting FlavorApp Monetization Setup...")
        
        # Create monetization models
        self.create_monetization_models()
        
        # Create monetization services
        self.create_monetization_services()
        
        # Update backend settings
        self.update_backend_settings()
        
        # Update frontend monetization services
        self.update_frontend_monetization()
        
        print("FlavorApp Monetization Setup Complete!")

if __name__ == '__main__':
    setup = FlavorAppMonetizationSetup()
    setup.main()
