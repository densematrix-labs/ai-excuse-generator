import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { LanguageSelector } from '../../components/LanguageSelector';

const mockChangeLanguage = vi.fn();

vi.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: {
      language: 'en',
      changeLanguage: mockChangeLanguage,
    },
  }),
}));

describe('LanguageSelector', () => {
  it('renders language selector', () => {
    render(<LanguageSelector />);
    const select = screen.getByRole('combobox');
    expect(select).toBeInTheDocument();
  });

  it('shows all 7 languages', () => {
    render(<LanguageSelector />);
    const options = screen.getAllByRole('option');
    expect(options).toHaveLength(7);
  });

  it('changes language on selection', () => {
    render(<LanguageSelector />);
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'zh' } });
    expect(mockChangeLanguage).toHaveBeenCalledWith('zh');
  });

  it('shows correct flag emojis', () => {
    render(<LanguageSelector />);
    expect(screen.getByText(/🇺🇸/)).toBeInTheDocument();
    expect(screen.getByText(/🇨🇳/)).toBeInTheDocument();
    expect(screen.getByText(/🇯🇵/)).toBeInTheDocument();
  });
});
