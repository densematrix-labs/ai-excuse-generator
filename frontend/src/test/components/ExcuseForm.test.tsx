import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ExcuseForm } from '../../components/ExcuseForm';

describe('ExcuseForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders the form with all elements', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={false} disabled={false} />);
    
    expect(screen.getByText('scenarios.title')).toBeInTheDocument();
    expect(screen.getByText('styles.title')).toBeInTheDocument();
    expect(screen.getByText('form.generate')).toBeInTheDocument();
  });

  it('shows custom scenario input when custom is selected', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={false} disabled={false} />);
    
    // Initially no custom input
    expect(screen.queryByPlaceholderText('form.customPlaceholder')).not.toBeInTheDocument();
    
    // Click custom scenario
    const customButton = screen.getByText('scenarios.custom').closest('button');
    fireEvent.click(customButton!);
    
    // Now custom input should appear
    expect(screen.getByPlaceholderText('form.customPlaceholder')).toBeInTheDocument();
  });

  it('submits form with correct data', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={false} disabled={false} />);
    
    // Fill target person
    const targetInput = screen.getByPlaceholderText('form.targetPlaceholder');
    fireEvent.change(targetInput, { target: { value: 'my boss' } });
    
    // Submit
    const submitButton = screen.getByText('form.generate').closest('button');
    fireEvent.click(submitButton!);
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      scenario: 'skip_work',
      customScenario: '',
      style: 'sincere',
      targetPerson: 'my boss',
      urgency: 3,
    });
  });

  it('shows loading state', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={true} disabled={false} />);
    
    expect(screen.getByText('form.generating')).toBeInTheDocument();
  });

  it('disables button when disabled prop is true', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={false} disabled={true} />);
    
    const submitButton = screen.getByRole('button', { name: /form.generate/i });
    expect(submitButton).toBeDisabled();
  });

  it('changes urgency with slider', () => {
    render(<ExcuseForm onSubmit={mockOnSubmit} isLoading={false} disabled={false} />);
    
    const slider = screen.getByRole('slider');
    fireEvent.change(slider, { target: { value: '5' } });
    
    const submitButton = screen.getByText('form.generate').closest('button');
    fireEvent.click(submitButton!);
    
    expect(mockOnSubmit).toHaveBeenCalledWith(
      expect.objectContaining({ urgency: 5 })
    );
  });
});
