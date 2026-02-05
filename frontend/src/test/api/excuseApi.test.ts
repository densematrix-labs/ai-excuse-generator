import { describe, it, expect, vi, beforeEach } from 'vitest';
import { generateExcuse, getTokenStatus, createCheckout } from '../../api/excuseApi';

describe('excuseApi', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('generateExcuse', () => {
    it('sends correct request and returns excuse', async () => {
      const mockResponse = {
        excuse: 'Test excuse',
        scenario: 'skip_work',
        style: 'sincere',
        remaining_tokens: 5,
        is_free_trial: false,
      };

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await generateExcuse({
        scenario: 'skip_work',
        style: 'sincere',
        urgency: 3,
        device_id: 'test-device',
        language: 'en',
      });

      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith('/api/excuse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: expect.any(String),
      });
    });

    it('throws error on failure', async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve({ detail: 'No tokens' }),
      });

      await expect(generateExcuse({
        scenario: 'skip_work',
        style: 'sincere',
        urgency: 3,
        device_id: 'test-device',
        language: 'en',
      })).rejects.toThrow('No tokens');
    });
  });

  describe('getTokenStatus', () => {
    it('returns token status', async () => {
      const mockStatus = {
        device_id: 'test-device',
        total_tokens: 10,
        used_tokens: 3,
        remaining_tokens: 7,
        free_trial_available: false,
      };

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockStatus),
      });

      const result = await getTokenStatus('test-device');

      expect(result).toEqual(mockStatus);
      expect(global.fetch).toHaveBeenCalledWith('/api/tokens/test-device');
    });

    it('throws error on failure', async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
      });

      await expect(getTokenStatus('test-device')).rejects.toThrow('Failed to get token status');
    });
  });

  describe('createCheckout', () => {
    it('returns checkout URL', async () => {
      const mockCheckout = {
        checkout_url: 'https://checkout.example.com',
        checkout_id: 'checkout_123',
      };

      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockCheckout),
      });

      const result = await createCheckout('product_1', 'device_1');

      expect(result).toEqual(mockCheckout);
      expect(global.fetch).toHaveBeenCalledWith('/api/payment/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: 'product_1', device_id: 'device_1' }),
      });
    });

    it('throws error on failure', async () => {
      (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValueOnce({
        ok: false,
      });

      await expect(createCheckout('product_1', 'device_1')).rejects.toThrow('Failed to create checkout');
    });
  });
});
