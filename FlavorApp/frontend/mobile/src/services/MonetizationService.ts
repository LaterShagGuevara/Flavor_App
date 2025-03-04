
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
