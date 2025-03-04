
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
