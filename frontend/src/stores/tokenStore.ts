import { create } from 'zustand';

interface TokenState {
  deviceId: string | null;
  totalTokens: number;
  usedTokens: number;
  remainingTokens: number;
  freeTrialAvailable: boolean;
  isLoading: boolean;
  setDeviceId: (id: string) => void;
  setTokenStatus: (status: Partial<TokenState>) => void;
  refreshTokens: () => Promise<void>;
}

export const useTokenStore = create<TokenState>((set, get) => ({
  deviceId: null,
  totalTokens: 0,
  usedTokens: 0,
  remainingTokens: 0,
  freeTrialAvailable: true,
  isLoading: false,

  setDeviceId: (id: string) => set({ deviceId: id }),

  setTokenStatus: (status: Partial<TokenState>) => set(status),

  refreshTokens: async () => {
    const { deviceId } = get();
    if (!deviceId) return;

    set({ isLoading: true });
    try {
      const response = await fetch(`/api/tokens/${deviceId}`);
      if (response.ok) {
        const data = await response.json();
        set({
          totalTokens: data.total_tokens,
          usedTokens: data.used_tokens,
          remainingTokens: data.remaining_tokens,
          freeTrialAvailable: data.free_trial_available,
        });
      }
    } catch (error) {
      console.error('Failed to refresh tokens:', error);
    } finally {
      set({ isLoading: false });
    }
  },
}));
