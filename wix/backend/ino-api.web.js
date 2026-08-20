import { auth } from '@wix/essentials';
import { secrets } from '@wix/secrets';
import { Permissions, webMethod } from '@wix/web-methods';
import { fetch } from 'wix-fetch';

const getSecretValue = auth.elevate(secrets.getSecretValue);

async function getSecret(name) {
  const { value } = await getSecretValue(name);
  if (!value) {
    throw new Error(`Missing Wix secret: ${name}`);
  }
  return value.replace(/\/$/, '');
}

async function parseResponse(response) {
  let payload;
  try {
    payload = await response.json();
  } catch (_error) {
    payload = {};
  }

  if (!response.ok) {
    const detail = payload.detail;
    const message =
      (typeof detail === 'string' && detail) ||
      detail?.message ||
      detail?.response ||
      payload.message ||
      'ino servisine şu anda ulaşılamıyor.';
    throw new Error(message);
  }

  return payload;
}

async function callApi(path, options = {}) {
  const apiBaseUrl = await getSecret('INO_API_BASE_URL');
  const response = await fetch(`${apiBaseUrl}${path}`, options);
  return parseResponse(response);
}

async function callPublicApi(path, options = {}) {
  const wixApiKey = await getSecret('INO_WIX_API_KEY');
  return callApi(path, {
    ...options,
    headers: {
      ...(options.headers || {}),
      'X-Wix-Key': wixApiKey,
    },
  });
}

export const sendChatMessage = webMethod(
  Permissions.Anyone,
  async (message, history = []) => {
    const safeMessage = String(message || '').trim();
    if (!safeMessage || safeMessage.length > 2000) {
      throw new Error('Mesaj 1-2000 karakter arasında olmalı.');
    }

    const safeHistory = Array.isArray(history) ? history.slice(-20) : [];
    return callPublicApi('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: safeMessage, history: safeHistory }),
    });
  },
);

export const submitDemoRequest = webMethod(
  Permissions.Anyone,
  async ({ name, number, note = '' }) => {
    return callPublicApi('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, number, note }),
    });
  },
);

export const getLeads = webMethod(
  Permissions.Admin,
  async () => {
    const adminApiKey = await getSecret('INO_ADMIN_API_KEY');
    return callApi('/api/leads', {
      method: 'GET',
      headers: { 'X-Admin-Key': adminApiKey },
    });
  },
);
