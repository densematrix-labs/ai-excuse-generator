import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import { useTokenStore } from '../stores/tokenStore';

interface PaymentSuccessProps {
  onBack: () => void;
}

export function PaymentSuccess({ onBack }: PaymentSuccessProps) {
  const { t } = useTranslation();
  const { refreshTokens, remainingTokens } = useTokenStore();

  useEffect(() => {
    refreshTokens();
  }, [refreshTokens]);

  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="text-center space-y-6 max-w-md mx-auto p-8">
        <div className="text-6xl">🎉</div>
        <h1 className="text-3xl font-bold text-gray-900">
          {t('payment.success.title')}
        </h1>
        <p className="text-gray-600 text-lg">
          {t('payment.success.subtitle')}
        </p>
        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-2xl p-6">
          <div className="text-5xl font-bold">{remainingTokens}</div>
          <div className="text-indigo-100">{t('payment.success.tokensAdded')}</div>
        </div>
        <button
          onClick={onBack}
          className="w-full py-4 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-all"
        >
          {t('payment.success.backToGenerator')}
        </button>
      </div>
    </div>
  );
}
