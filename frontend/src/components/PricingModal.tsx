import { useTranslation } from 'react-i18next';
import { createCheckout } from '../api/excuseApi';
import { useTokenStore } from '../stores/tokenStore';
import { useState } from 'react';

interface PricingModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const products = [
  { id: 'excuse_3pack', tokens: 3, priceKey: 'starter' },
  { id: 'excuse_10pack', tokens: 10, priceKey: 'regular', popular: true },
  { id: 'excuse_30pack', tokens: 30, priceKey: 'pro' },
];

export function PricingModal({ isOpen, onClose }: PricingModalProps) {
  const { t } = useTranslation();
  const { deviceId } = useTokenStore();
  const [loading, setLoading] = useState<string | null>(null);

  if (!isOpen) return null;

  const handlePurchase = async (productId: string) => {
    if (!deviceId) return;
    
    setLoading(productId);
    try {
      const result = await createCheckout(productId, deviceId);
      window.location.href = result.checkout_url;
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Failed to create checkout. Please try again.');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{t('pricing.title')}</h2>
              <p className="text-gray-600">{t('pricing.subtitle')}</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <div className="p-6">
          <div className="grid sm:grid-cols-3 gap-4">
            {products.map((product) => (
              <div
                key={product.id}
                className={`relative rounded-xl border-2 p-5 ${
                  product.popular
                    ? 'border-indigo-500 bg-indigo-50'
                    : 'border-gray-200 bg-white'
                }`}
              >
                {product.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap">
                    {t(`pricing.${product.priceKey}.popular`)}
                  </span>
                )}
                <div className="text-center space-y-3">
                  <h3 className="font-bold text-lg text-gray-900">
                    {t(`pricing.${product.priceKey}.name`)}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {t(`pricing.${product.priceKey}.description`)}
                  </p>
                  <div className="text-3xl font-bold text-indigo-600">
                    {t(`pricing.${product.priceKey}.price`)}
                  </div>
                  <button
                    onClick={() => handlePurchase(product.id)}
                    disabled={loading === product.id}
                    className={`w-full py-3 rounded-xl font-medium transition-all ${
                      product.popular
                        ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    } disabled:opacity-50`}
                  >
                    {loading === product.id ? '...' : t('pricing.buy')}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
