import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TokenDisplay } from '../../components/TokenDisplay';
import { useTokenStore } from '../../stores/tokenStore';

vi.mock('../../stores/tokenStore');

describe('TokenDisplay', () => {
  const mockOnBuyMore = vi.fn();
  const mockUseTokenStore = useTokenStore as unknown as ReturnType<typeof vi.fn>;

  beforeEach(() => {
    mockOnBuyMore.mockClear();
  });

  it('shows free trial available', () => {
    mockUseTokenStore.mockReturnValue({
      remainingTokens: 0,
      freeTrialAvailable: true,
    });

    render(<TokenDisplay onBuyMore={mockOnBuyMore} />);
    
    expect(screen.getByText('tokens.freeTrialAvailable')).toBeInTheDocument();
  });

  it('shows remaining tokens count', () => {
    mockUseTokenStore.mockReturnValue({
      remainingTokens: 5,
      freeTrialAvailable: false,
    });

    render(<TokenDisplay onBuyMore={mockOnBuyMore} />);
    
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('shows buy more button when no tokens', () => {
    mockUseTokenStore.mockReturnValue({
      remainingTokens: 0,
      freeTrialAvailable: false,
    });

    render(<TokenDisplay onBuyMore={mockOnBuyMore} />);
    
    const buyButton = screen.getByText('tokens.buyMore');
    expect(buyButton).toBeInTheDocument();
    
    fireEvent.click(buyButton);
    expect(mockOnBuyMore).toHaveBeenCalled();
  });

  it('does not show buy more button when has tokens', () => {
    mockUseTokenStore.mockReturnValue({
      remainingTokens: 10,
      freeTrialAvailable: false,
    });

    render(<TokenDisplay onBuyMore={mockOnBuyMore} />);
    
    expect(screen.queryByText('tokens.buyMore')).not.toBeInTheDocument();
  });
});
