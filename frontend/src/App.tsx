import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { LanguageSelector } from './components/LanguageSelector';
import { TokenDisplay } from './components/TokenDisplay';
import { ExcuseForm } from './components/ExcuseForm';
import { ExcuseResult } from './components/ExcuseResult';
import { PricingModal } from './components/PricingModal';
import { PaymentSuccess } from './components/PaymentSuccess';
import { useTokenStore } from './stores/tokenStore';
import { getDeviceId } from './utils/fingerprint';
import { generateExcuse, ExcuseResponse } from './api/excuseApi';

type Page = 'generator' | 'payment-success';

function App() {
  const { t, i18n } = useTranslation();
  const [page, setPage] = useState<Page>('generator');
  const [excuse, setExcuse] = useState<ExcuseResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPricing, setShowPricing] = useState(false);
  
  const { 
    setDeviceId, 
    refreshTokens, 
    deviceId,
    freeTrialAvailable,
    remainingTokens 
  } = useTokenStore();

  // Check for payment success URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('payment') === 'success') {
      setPage('payment-success');
      window.history.replaceState({}, '', '/');
    }
  }, []);

  // Initialize device ID
  useEffect(() => {
    const init = async () => {
      const id = await getDeviceId();
      setDeviceId(id);
    };
    init();
  }, [setDeviceId]);

  // Fetch token status when device ID is set
  useEffect(() => {
    if (deviceId) {
      refreshTokens();
    }
  }, [deviceId, refreshTokens]);

  const canGenerate = freeTrialAvailable || remainingTokens > 0;

  const handleGenerate = async (data: {
    scenario: string;
    customScenario: string;
    style: string;
    targetPerson: string;
    urgency: number;
  }) => {
    if (!deviceId || !canGenerate) {
      setShowPricing(true);
      return;
    }

    setIsLoading(true);
    setError(null);
    setExcuse(null);

    try {
      const result = await generateExcuse({
        scenario: data.scenario,
        custom_scenario: data.customScenario || undefined,
        style: data.style,
        target_person: data.targetPerson || undefined,
        urgency: data.urgency,
        device_id: deviceId,
        language: i18n.language?.split('-')[0] || 'en',
      });
      setExcuse(result);
      refreshTokens();
    } catch (err) {
      const message = err instanceof Error ? err.message : t('errors.generation');
      if (message.includes('No tokens') || message.includes('402')) {
        setShowPricing(true);
      } else {
        setError(message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (page === 'payment-success') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
        <div className="container mx-auto px-4 py-8">
          <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
            <PaymentSuccess onBack={() => setPage('generator')} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-4xl">🎭</span>
            <h1 className="text-2xl font-bold text-white">{t('app.title')}</h1>
          </div>
          <div className="flex items-center gap-4">
            <TokenDisplay onBuyMore={() => setShowPricing(true)} />
            <LanguageSelector />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 pb-12">
        <div className="max-w-2xl mx-auto">
          {/* Tagline */}
          <div className="text-center mb-8">
            <p className="text-xl text-white/90">{t('app.tagline')}</p>
          </div>

          {/* Card */}
          <div className="bg-white rounded-3xl shadow-2xl p-6 sm:p-8 space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
                {error}
              </div>
            )}

            {excuse ? (
              <ExcuseResult
                excuse={excuse.excuse}
                isFreeTrial={excuse.is_free_trial}
                onTryAnother={() => setExcuse(null)}
              />
            ) : (
              <ExcuseForm
                onSubmit={handleGenerate}
                isLoading={isLoading}
                disabled={!canGenerate}
              />
            )}

            {!canGenerate && !excuse && (
              <div className="text-center p-4 bg-amber-50 rounded-xl">
                <p className="text-amber-800 mb-3">{t('errors.noTokens')}</p>
                <button
                  onClick={() => setShowPricing(true)}
                  className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-6 py-2 rounded-full font-medium hover:from-amber-600 hover:to-orange-600 transition-all"
                >
                  {t('tokens.buyMore')}
                </button>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-6 text-center">
        <p className="text-white/70 text-sm">
          {t('footer.poweredBy')} • {t('footer.disclaimer')}
        </p>
      </footer>

      {/* Pricing Modal */}
      <PricingModal isOpen={showPricing} onClose={() => setShowPricing(false)} />
    </div>
  );
}

export default App;
