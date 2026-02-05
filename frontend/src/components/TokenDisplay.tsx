import { useTranslation } from 'react-i18next';
import { useTokenStore } from '../stores/tokenStore';

interface TokenDisplayProps {
  onBuyMore: () => void;
}

export function TokenDisplay({ onBuyMore }: TokenDisplayProps) {
  const { t } = useTranslation();
  const { remainingTokens, freeTrialAvailable } = useTokenStore();

  const hasTokens = remainingTokens > 0 || freeTrialAvailable;

  return (
    <div className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-full px-4 py-2">
      <div className="flex items-center gap-2">
        <span className="text-2xl">🎫</span>
        <span className="text-white font-medium">
          {freeTrialAvailable ? (
            t('tokens.freeTrialAvailable')
          ) : (
            <>
              {t('tokens.remaining')}: <span className="font-bold">{remainingTokens}</span>
            </>
          )}
        </span>
      </div>
      {!hasTokens && (
        <button
          onClick={onBuyMore}
          className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-medium hover:from-amber-600 hover:to-orange-600 transition-all whitespace-nowrap"
        >
          {t('tokens.buyMore')}
        </button>
      )}
    </div>
  );
}
