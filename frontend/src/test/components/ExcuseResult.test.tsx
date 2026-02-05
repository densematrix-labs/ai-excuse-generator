import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ExcuseResult } from '../../components/ExcuseResult';

describe('ExcuseResult', () => {
  const mockOnTryAnother = vi.fn();
  const testExcuse = 'Sorry, my cat scheduled an emergency therapy session.';

  beforeEach(() => {
    mockOnTryAnother.mockClear();
    vi.clearAllMocks();
  });

  it('renders the excuse text', () => {
    render(
      <ExcuseResult
        excuse={testExcuse}
        isFreeTrial={false}
        onTryAnother={mockOnTryAnother}
      />
    );
    
    expect(screen.getByText(testExcuse)).toBeInTheDocument();
  });

  it('shows free trial badge when applicable', () => {
    render(
      <ExcuseResult
        excuse={testExcuse}
        isFreeTrial={true}
        onTryAnother={mockOnTryAnother}
      />
    );
    
    expect(screen.getByText('result.freeTrialUsed')).toBeInTheDocument();
  });

  it('does not show free trial badge when not free trial', () => {
    render(
      <ExcuseResult
        excuse={testExcuse}
        isFreeTrial={false}
        onTryAnother={mockOnTryAnother}
      />
    );
    
    expect(screen.queryByText('result.freeTrialUsed')).not.toBeInTheDocument();
  });

  it('copies text to clipboard on copy button click', async () => {
    render(
      <ExcuseResult
        excuse={testExcuse}
        isFreeTrial={false}
        onTryAnother={mockOnTryAnother}
      />
    );
    
    const copyButton = screen.getByText('result.copy').closest('button');
    fireEvent.click(copyButton!);
    
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(testExcuse);
    
    await waitFor(() => {
      expect(screen.getByText('result.copied')).toBeInTheDocument();
    });
  });

  it('calls onTryAnother when try another button clicked', () => {
    render(
      <ExcuseResult
        excuse={testExcuse}
        isFreeTrial={false}
        onTryAnother={mockOnTryAnother}
      />
    );
    
    const tryAnotherButton = screen.getByText('result.tryAnother').closest('button');
    fireEvent.click(tryAnotherButton!);
    
    expect(mockOnTryAnother).toHaveBeenCalled();
  });
});
