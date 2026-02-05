import { useTranslation } from 'react-i18next';

const scenarios = [
  { id: 'skip_work', emoji: '💼' },
  { id: 'avoid_party', emoji: '🎉' },
  { id: 'late_arrival', emoji: '⏰' },
  { id: 'forgot_task', emoji: '📝' },
  { id: 'cancel_plans', emoji: '📅' },
  { id: 'miss_meeting', emoji: '🤝' },
  { id: 'custom', emoji: '✨' },
];

interface ScenarioSelectorProps {
  selected: string;
  onSelect: (scenario: string) => void;
}

export function ScenarioSelector({ selected, onSelect }: ScenarioSelectorProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-gray-800">{t('scenarios.title')}</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            onClick={() => onSelect(scenario.id)}
            className={`flex items-center gap-2 px-4 py-3 rounded-xl border-2 transition-all ${
              selected === scenario.id
                ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
            }`}
          >
            <span className="text-xl">{scenario.emoji}</span>
            <span className="font-medium text-sm truncate">
              {t(`scenarios.${scenario.id}`)}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
