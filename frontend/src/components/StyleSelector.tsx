import { useTranslation } from 'react-i18next';

const styles = [
  { id: 'sincere', emoji: '🥺', color: 'blue' },
  { id: 'professional', emoji: '👔', color: 'gray' },
  { id: 'creative', emoji: '🎨', color: 'purple' },
  { id: 'dramatic', emoji: '🎭', color: 'red' },
  { id: 'absurd', emoji: '🤪', color: 'yellow' },
];

interface StyleSelectorProps {
  selected: string;
  onSelect: (style: string) => void;
}

export function StyleSelector({ selected, onSelect }: StyleSelectorProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold text-gray-800">{t('styles.title')}</h3>
      <div className="flex flex-wrap gap-2">
        {styles.map((style) => (
          <button
            key={style.id}
            onClick={() => onSelect(style.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full border-2 transition-all ${
              selected === style.id
                ? 'border-indigo-500 bg-indigo-500 text-white'
                : 'border-gray-200 hover:border-indigo-300 bg-white'
            }`}
          >
            <span>{style.emoji}</span>
            <span className="font-medium">{t(`styles.${style.id}`)}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
