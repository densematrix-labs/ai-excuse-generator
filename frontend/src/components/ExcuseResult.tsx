import { useState } from 'react';
import { useTranslation } from 'react-i18next';

interface ExcuseResultProps {
  excuse: string;
  isFreeTrial: boolean;
  onTryAnother: () => void;
}

export function ExcuseResult({ excuse, isFreeTrial, onTryAnother }: ExcuseResultProps) {
  const { t } = useTranslation();
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(excuse);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <span>✨</span>
          {t('result.title')}
        </h3>
        {isFreeTrial && (
          <span className="text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full">
            {t('result.freeTrialUsed')}
          </span>
        )}
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm">
        <p className="text-gray-800 text-lg leading-relaxed whitespace-pre-wrap">{excuse}</p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleCopy}
          className="flex-1 py-3 px-4 bg-white border-2 border-indigo-200 text-indigo-600 font-medium rounded-xl hover:bg-indigo-50 transition-all flex items-center justify-center gap-2"
        >
          {copied ? (
            <>
              <span>✅</span>
              {t('result.copied')}
            </>
          ) : (
            <>
              <span>📋</span>
              {t('result.copy')}
            </>
          )}
        </button>
        <button
          onClick={onTryAnother}
          className="flex-1 py-3 px-4 bg-indigo-600 text-white font-medium rounded-xl hover:bg-indigo-700 transition-all flex items-center justify-center gap-2"
        >
          <span>🔄</span>
          {t('result.tryAnother')}
        </button>
      </div>
    </div>
  );
}
