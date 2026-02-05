import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { StyleSelector } from '../../components/StyleSelector';

describe('StyleSelector', () => {
  const mockOnSelect = vi.fn();

  beforeEach(() => {
    mockOnSelect.mockClear();
  });

  it('renders all styles', () => {
    render(<StyleSelector selected="sincere" onSelect={mockOnSelect} />);
    
    expect(screen.getByText('styles.sincere')).toBeInTheDocument();
    expect(screen.getByText('styles.professional')).toBeInTheDocument();
    expect(screen.getByText('styles.creative')).toBeInTheDocument();
    expect(screen.getByText('styles.dramatic')).toBeInTheDocument();
    expect(screen.getByText('styles.absurd')).toBeInTheDocument();
  });

  it('highlights selected style', () => {
    render(<StyleSelector selected="absurd" onSelect={mockOnSelect} />);
    
    const absurdButton = screen.getByText('styles.absurd').closest('button');
    expect(absurdButton).toHaveClass('bg-indigo-500');
  });

  it('calls onSelect when clicking style', () => {
    render(<StyleSelector selected="sincere" onSelect={mockOnSelect} />);
    
    const dramaticButton = screen.getByText('styles.dramatic').closest('button');
    fireEvent.click(dramaticButton!);
    
    expect(mockOnSelect).toHaveBeenCalledWith('dramatic');
  });

  it('shows emojis for each style', () => {
    render(<StyleSelector selected="sincere" onSelect={mockOnSelect} />);
    
    expect(screen.getByText('🥺')).toBeInTheDocument();
    expect(screen.getByText('🎭')).toBeInTheDocument();
    expect(screen.getByText('🤪')).toBeInTheDocument();
  });
});
