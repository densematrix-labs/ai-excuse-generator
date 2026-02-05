import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { ScenarioSelector } from './ScenarioSelector';
import { StyleSelector } from './StyleSelector';

interface ExcuseFormProps {
  onSubmit: (data: {
    scenario: string;
    customScenario: string;
    style: string;
    targetPerson: string;
    urgency: number;
  }) => void;
  isLoading: boolean;
  disabled: boolean;
}

export function ExcuseForm({ onSubmit, isLoading, disabled }: ExcuseFormProps) {
  const { t } = useTranslation();
  const [scenario, setScenario] = useState('skip_work');
  const [customScenario, setCustomScenario] = useState('');
  const [style, setStyle] = useState('sincere');
  const [targetPerson, setTargetPerson] = useState('');
  const [urgency, setUrgency] = useState(3);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ scenario, customScenario, style, targetPerson, urgency });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <ScenarioSelector selected={scenario} onSelect={setScenario} />

      {scenario === 'custom' && (
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">
            {t('form.customScenario')}
          </label>
          <input
            type="text"
            value={customScenario}
            onChange={(e) => setCustomScenario(e.target.value)}
            placeholder={t('form.customPlaceholder')}
            className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all"
            maxLength={200}
          />
        </div>
      )}

      <StyleSelector selected={style} onSelect={setStyle} />

      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          {t('form.targetPerson')}
        </label>
        <input
          type="text"
          value={targetPerson}
          onChange={(e) => setTargetPerson(e.target.value)}
          placeholder={t('form.targetPlaceholder')}
          className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all"
          maxLength={50}
        />
      </div>

      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          {t('form.urgency')}: {urgency}
        </label>
        <input
          type="range"
          min="1"
          max="5"
          value={urgency}
          onChange={(e) => setUrgency(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>😌</span>
          <span>😅</span>
          <span>😰</span>
          <span>😱</span>
          <span>🆘</span>
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading || disabled}
        className="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold text-lg rounded-xl hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02] active:scale-[0.98]"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            {t('form.generating')}
          </span>
        ) : (
          <span className="flex items-center justify-center gap-2">
            <span>🎭</span>
            {t('form.generate')}
          </span>
        )}
      </button>
    </form>
  );
}
