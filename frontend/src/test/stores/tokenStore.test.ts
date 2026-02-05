import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useTokenStore } from '../../stores/tokenStore';

describe('tokenStore', () => {
  beforeEach(() => {
    useTokenStore.setState({
      deviceId: null,
      totalTokens: 0,
      usedTokens: 0,
      remainingTokens: 0,
      freeTrialAvailable: true,
      isLoading: false,
    });
    vi.clearAllMocks();
  });

  it('sets device ID', () => {
    const { setDeviceId } = useTokenStore.getState();
    setDeviceId('test-device-123');
    
    expect(useTokenStore.getState().deviceId).toBe('test-device-123');
  });

  it('sets token status', () => {
    const { setTokenStatus } = useTokenStore.getState();
    setTokenStatus({
      totalTokens: 10,
      usedTokens: 3,
      remainingTokens: 7,
      freeTrialAvailable: false,
    });
    
    const state = useTokenStore.getState();
    expect(state.totalTokens).toBe(10);
    expect(state.usedTokens).toBe(3);
    expect(state.remainingTokens).toBe(7);
    expect(state.freeTrialAvailable).toBe(false);
  });

  it('refreshes tokens from API', async () => {
    const mockResponse = {
      total_tokens: 15,
      used_tokens: 5,
      remaining_tokens: 10,
      free_trial_available: false,
    };

    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const { setDeviceId, refreshTokens } = useTokenStore.getState();
    setDeviceId('test-device');
    
    await refreshTokens();
    
    const state = useTokenStore.getState();
    expect(state.totalTokens).toBe(15);
    expect(state.remainingTokens).toBe(10);
  });

  it('does not refresh without device ID', async () => {
    const { refreshTokens } = useTokenStore.getState();
    
    await refreshTokens();
    
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('handles refresh error gracefully', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error('Network error'));

    const { setDeviceId, refreshTokens } = useTokenStore.getState();
    setDeviceId('test-device');
    
    await refreshTokens();
    
    // Should not throw, state unchanged
    expect(useTokenStore.getState().totalTokens).toBe(0);
  });
});
