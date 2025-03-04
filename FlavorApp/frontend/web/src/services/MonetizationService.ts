
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
