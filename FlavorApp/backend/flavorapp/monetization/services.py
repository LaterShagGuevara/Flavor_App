
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
