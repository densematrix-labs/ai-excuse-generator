import FingerprintJS from '@fingerprintjs/fingerprintjs';

let cachedFingerprint: string | null = null;

export async function getDeviceId(): Promise<string> {
  if (cachedFingerprint) {
    return cachedFingerprint;
  }

  try {
    const fp = await FingerprintJS.load();
    const result = await fp.get();
    cachedFingerprint = result.visitorId;
    return cachedFingerprint;
  } catch (error) {
    console.error('Fingerprint error:', error);
    // Fallback to random ID stored in localStorage
    let fallbackId = localStorage.getItem('excuse_device_id');
    if (!fallbackId) {
      fallbackId = 'fallback_' + Math.random().toString(36).substring(2, 15) + Date.now().toString(36);
      localStorage.setItem('excuse_device_id', fallbackId);
    }
    cachedFingerprint = fallbackId;
    return fallbackId;
  }
}
