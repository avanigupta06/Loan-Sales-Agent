const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async newSession() {
    const res = await fetch(`${BASE_URL}/session/new`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to start session');
    return res.json();
  },

  async chat(sessionId, message) {
    const res = await fetch(`${BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
    if (!res.ok) throw new Error('Chat request failed');
    return res.json();
  },

  async uploadSalarySlip(sessionId, file) {
    const form = new FormData();
    form.append('session_id', sessionId);
    form.append('file', file);
    const res = await fetch(`${BASE_URL}/upload`, { method: 'POST', body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Upload failed');
    }
    return res.json();
  },

  getPdfUrl(sessionId) {
    return `${BASE_URL}/generate-pdf/${sessionId}`;
  },

  async getCustomers() {
    const res = await fetch(`${BASE_URL}/mock/customers`);
    return res.json();
  },
};
