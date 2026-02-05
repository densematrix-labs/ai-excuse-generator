import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ScenarioSelector } from '../../components/ScenarioSelector';

describe('ScenarioSelector', () => {
  const mockOnSelect = vi.fn();

  beforeEach(() => {
    mockOnSelect.mockClear();
  });

  it('renders all scenarios', () => {
    render(<ScenarioSelector selected="skip_work" onSelect={mockOnSelect} />);
    
    expect(screen.getByText('scenarios.skip_work')).toBeInTheDocument();
    expect(screen.getByText('scenarios.avoid_party')).toBeInTheDocument();
    expect(screen.getByText('scenarios.late_arrival')).toBeInTheDocument();
    expect(screen.getByText('scenarios.custom')).toBeInTheDocument();
  });

  it('highlights selected scenario', () => {
    render(<ScenarioSelector selected="skip_work" onSelect={mockOnSelect} />);
    
    const buttons = screen.getAllByRole('button');
    const skipWorkButton = buttons.find(b => b.textContent?.includes('scenarios.skip_work'));
    expect(skipWorkButton).toHaveClass('border-indigo-500');
  });

  it('calls onSelect when clicking scenario', () => {
    render(<ScenarioSelector selected="skip_work" onSelect={mockOnSelect} />);
    
    const avoidPartyButton = screen.getByText('scenarios.avoid_party').closest('button');
    fireEvent.click(avoidPartyButton!);
    
    expect(mockOnSelect).toHaveBeenCalledWith('avoid_party');
  });

  it('shows emojis for each scenario', () => {
    render(<ScenarioSelector selected="skip_work" onSelect={mockOnSelect} />);
    
    expect(screen.getByText('💼')).toBeInTheDocument();
    expect(screen.getByText('🎉')).toBeInTheDocument();
    expect(screen.getByText('⏰')).toBeInTheDocument();
  });
});
