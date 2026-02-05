export interface ExcuseRequest {
  scenario: string;
  custom_scenario?: string;
  style: string;
  target_person?: string;
  urgency: number;
  device_id: string;
  language: string;
}

export interface ExcuseResponse {
  excuse: string;
  scenario: string;
  style: string;
  remaining_tokens: number;
  is_free_trial: boolean;
}

export interface TokenStatus {
  device_id: string;
  total_tokens: number;
  used_tokens: number;
  remaining_tokens: number;
  free_trial_available: boolean;
}

export interface CheckoutResponse {
  checkout_url: string;
  checkout_id: string;
}

export async function generateExcuse(request: ExcuseRequest): Promise<ExcuseResponse> {
  const response = await fetch('/api/excuse', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate excuse');
  }

  return response.json();
}

export async function getTokenStatus(deviceId: string): Promise<TokenStatus> {
  const response = await fetch(`/api/tokens/${deviceId}`);
  if (!response.ok) {
    throw new Error('Failed to get token status');
  }
  return response.json();
}

export async function createCheckout(productId: string, deviceId: string): Promise<CheckoutResponse> {
  const response = await fetch('/api/payment/checkout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: productId,
      device_id: deviceId,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to create checkout');
  }

  return response.json();
}
