import { useTranslation } from 'react-i18next';

const languages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
];

export function LanguageSelector() {
  const { i18n, t } = useTranslation();

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    i18n.changeLanguage(e.target.value);
  };

  return (
    <div className="relative">
      <label htmlFor="language-select" className="sr-only">
        {t('language.select')}
      </label>
      <select
        id="language-select"
        value={i18n.language?.split('-')[0] || 'en'}
        onChange={handleChange}
        className="appearance-none bg-white/10 backdrop-blur-sm border border-white/20 text-white rounded-lg px-4 py-2 pr-8 cursor-pointer hover:bg-white/20 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code} className="text-gray-900">
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
      <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
  );
}
