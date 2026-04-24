import React, { useState, useRef, useEffect, useCallback } from 'react';
import { MINI_FAQS } from '../utils/miniFaqs';
import { renderMarkdown } from '../utils/markdown';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const KEYFRAMES = `
@keyframes mc-fadein { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none} }
@keyframes mc-dot    { 0%,80%,100%{transform:scale(0.65);opacity:0.4} 40%{transform:scale(1);opacity:1} }
@keyframes mc-pulse  { 0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.15);opacity:0.7} }
`;

function injectKeyframes() {
  if (document.getElementById('mc-keyframes')) return;
  const el = document.createElement('style');
  el.id = 'mc-keyframes';
  el.textContent = KEYFRAMES;
  document.head.appendChild(el);
}

const S = {
  fab: (open) => ({
    position: 'fixed',
    bottom: '90px',
    right: '24px',
    width: '52px',
    height: '52px',
    borderRadius: '50%',
    background: open
      ? 'linear-gradient(135deg, #1e3a5f, #1a4fcc)'
      : 'linear-gradient(135deg, #2563eb, #1d4ed8)',
    border: '1.5px solid rgba(59,130,246,0.45)',
    boxShadow: open ? '0 2px 12px rgba(29,78,216,0.3)' : '0 4px 20px rgba(29,78,216,0.5)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    cursor: 'pointer',
    zIndex: 10000,
    transition: 'transform 0.2s ease, box-shadow 0.2s ease',
    transform: 'scale(1)',
    outline: 'none', flexShrink: 0,
  }),

  badge: {
    position: 'absolute', top: '0px', right: '0px',
    width: '13px', height: '13px', borderRadius: '50%',
    background: '#ef4444', border: '2px solid #0d1117',
    animation: 'mc-pulse 2s ease-in-out infinite', pointerEvents: 'none',
  },

  /* bottom: 90 (FAB bottom) + 52 (FAB height) + 12 (gap) = 154px */
  panel: (visible) => ({
    position: 'fixed',
    bottom: '154px',
    right: '16px',
    width: '370px',
    maxWidth: 'calc(100vw - 32px)',
    height: '540px',
    maxHeight: 'calc(100vh - 110px)',
    background: '#161b22',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '18px',
    boxShadow: '0 24px 64px rgba(0,0,0,0.55)',
    display: 'flex', flexDirection: 'column',
    zIndex: 9999, overflow: 'hidden',
    opacity: visible ? 1 : 0,
    transform: visible ? 'translateY(0) scale(1)' : 'translateY(14px) scale(0.97)',
    pointerEvents: visible ? 'all' : 'none',
    transition: 'opacity 0.2s ease, transform 0.2s ease',
  }),

  panelHeader: {
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    padding: '12px 14px',
    background: 'linear-gradient(135deg, #1c2740, #181f2e)',
    borderBottom: '1px solid rgba(255,255,255,0.07)',
    flexShrink: 0, minHeight: '58px',
  },

  headerLeft: { display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0 },

  avatar: {
    width: '34px', height: '34px', minWidth: '34px', borderRadius: '10px',
    background: 'linear-gradient(135deg, #1e3a5f, #2563eb)',
    border: '1px solid rgba(59,130,246,0.3)',
    display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '17px',
  },

  headerText: { display: 'flex', flexDirection: 'column', gap: '2px' },
  headerTitle: { fontSize: '13px', fontWeight: 700, color: '#f0f6fc', lineHeight: 1 },
  headerSub: { fontSize: '10px', color: '#4a5568', display: 'flex', alignItems: 'center', gap: '5px' },
  onlineDot: { width: '6px', height: '6px', minWidth: '6px', borderRadius: '50%', background: '#10b981' },

  headerRight: { display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 },

  clearBtn: {
    background: 'none', border: 'none', color: '#4a5568',
    fontSize: '11px', fontWeight: 600, cursor: 'pointer',
    fontFamily: 'inherit', padding: '5px 8px', borderRadius: '6px',
    transition: 'color 0.15s, background 0.15s', lineHeight: 1, outline: 'none',
  },

  closeBtn: {
    width: '28px', height: '28px', minWidth: '28px', borderRadius: '8px',
    background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)',
    cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
    transition: 'background 0.15s', outline: 'none', flexShrink: 0,
  },

  messages: {
    flex: 1, overflowY: 'auto', padding: '14px 14px 8px',
    display: 'flex', flexDirection: 'column', gap: '10px',
  },

  bubbleWrap: (isUser) => ({
    display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start',
    animation: 'mc-fadein 0.22s ease-out both',
  }),

  botLabel: { fontSize: '10px', color: '#3d4f6b', fontWeight: 600, marginBottom: '3px', paddingLeft: '2px' },

  bubble: (isUser) => ({
    maxWidth: '88%', padding: '9px 12px',
    borderRadius: isUser ? '14px 14px 3px 14px' : '14px 14px 14px 3px',
    background: isUser ? 'linear-gradient(135deg, #2563eb, #1d4ed8)' : '#1c2332',
    border: `1px solid ${isUser ? 'rgba(59,130,246,0.25)' : 'rgba(255,255,255,0.07)'}`,
    fontSize: '13px', lineHeight: '1.6', color: '#e8edf4', wordBreak: 'break-word',
  }),

  typingWrap: {
    display: 'flex', alignItems: 'center', gap: '4px', padding: '9px 13px',
    background: '#1c2332', border: '1px solid rgba(255,255,255,0.07)',
    borderRadius: '14px 14px 14px 3px', width: 'fit-content',
  },

  typingDot: (i) => ({
    width: '6px', height: '6px', borderRadius: '50%', background: '#4a7fd4',
    display: 'inline-block', animation: 'mc-dot 1.2s ease-in-out infinite',
    animationDelay: `${i * 0.2}s`,
  }),

  faqRow: {
    display: 'flex', flexWrap: 'wrap', gap: '6px', padding: '8px 14px 10px',
    borderTop: '1px solid rgba(255,255,255,0.05)', flexShrink: 0,
  },

  faqChip: {
    padding: '5px 11px', background: 'rgba(37,99,235,0.1)',
    border: '1px solid rgba(37,99,235,0.22)', borderRadius: '20px',
    fontSize: '11px', fontWeight: 600, color: '#60a5fa',
    cursor: 'pointer', fontFamily: 'inherit', lineHeight: 1.4,
    transition: 'all 0.15s', whiteSpace: 'nowrap', outline: 'none',
  },

  /* KEY FIX: alignItems:'center' keeps send button aligned with textarea, not overlapping */
  inputBar: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '10px 12px 12px',
    borderTop: '1px solid rgba(255,255,255,0.07)',
    background: '#161b22',
    flexShrink: 0,
  },

  textarea: {
    flex: 1,
    minWidth: 0,
    background: '#1e2533',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '12px',
    padding: '9px 12px',
    fontSize: '13px', color: '#f0f6fc',
    fontFamily: 'inherit', resize: 'none', outline: 'none',
    lineHeight: '1.5', minHeight: '38px', maxHeight: '90px',
    overflowY: 'auto', transition: 'border-color 0.15s', display: 'block',
  },

  sendBtn: (active) => ({
    width: '38px', height: '38px', minWidth: '38px',
    borderRadius: '11px',
    background: active ? 'linear-gradient(135deg, #2563eb, #1d4ed8)' : '#1e2533',
    border: `1px solid ${active ? 'rgba(59,130,246,0.4)' : 'rgba(255,255,255,0.08)'}`,
    color: active ? '#fff' : '#3d4f6b',
    cursor: active ? 'pointer' : 'not-allowed',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    flexShrink: 0, transition: 'all 0.15s', outline: 'none',
    boxShadow: active ? '0 2px 10px rgba(37,99,235,0.35)' : 'none',
  }),

  footer: {
    fontSize: '10px', color: '#252e3f', textAlign: 'center',
    padding: '4px 0 6px', flexShrink: 0, letterSpacing: '0.3px',
  },
};

export default function MiniChatbot() {
  const [open, setOpen]           = useState(false);
  const [visible, setVisible]     = useState(false);
  const [input, setInput]         = useState('');
  const [loading, setLoading]     = useState(false);
  const [showBadge, setShowBadge] = useState(true);
  const [messages, setMessages]   = useState([{
    id: 0, role: 'assistant',
    content: "Hi! I'm your **Finance Assistant** 💰\n\nAsk me anything about loans, EMI, interest rates, or credit scores.\n\nOr tap a quick question below 👇",
  }]);

  const msgsRef     = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => { injectKeyframes(); }, []);

  useEffect(() => {
    if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight;
  }, [messages, loading]);

  const handleToggle = () => {
    if (!open) {
      setOpen(true); setShowBadge(false);
      requestAnimationFrame(() => requestAnimationFrame(() => setVisible(true)));
    } else {
      setVisible(false);
      setTimeout(() => setOpen(false), 210);
    }
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    const ta = e.target;
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 90) + 'px';
  };

  const sendMessage = useCallback(async (text) => {
    const query = (text || input).trim();
    if (!query || loading) return;
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = '38px';
    const history = messages.filter(m => m.id !== 0).map(m => ({ role: m.role, content: m.content }));
    setMessages(prev => [...prev, { id: Date.now(), role: 'user', content: query }]);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/mini-chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, history }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'assistant', content: data.answer }]);
    } catch {
      setMessages(prev => [...prev, {
        id: Date.now() + 1, role: 'assistant',
        content: "⚠️ Couldn't reach the server. Make sure the backend is running on port 8000.",
      }]);
    } finally { setLoading(false); }
  }, [input, loading, messages]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const clearChat = () => setMessages([{
    id: 0, role: 'assistant', content: "Chat cleared! Ask me anything about loans, EMI, or finance. 💡",
  }]);

  const canSend = input.trim().length > 0 && !loading;

  return (
    <>
      {/* Panel renders before FAB so FAB has higher paint order */}
      {open && (
        <div style={S.panel(visible)}>

          {/* Header */}
          <div style={S.panelHeader}>
            <div style={S.headerLeft}>
              <div style={S.avatar}>💰</div>
              <div style={S.headerText}>
                <span style={S.headerTitle}>Finance Assistant</span>
                <span style={S.headerSub}>
                  <span style={S.onlineDot} />
                  Online · Loan Sale AI System
                </span>
              </div>
            </div>
            <div style={S.headerRight}>
              <button style={S.clearBtn} onClick={clearChat} title="Clear chat"
                onMouseEnter={e => { e.currentTarget.style.color='#8b949e'; e.currentTarget.style.background='rgba(255,255,255,0.06)'; }}
                onMouseLeave={e => { e.currentTarget.style.color='#4a5568'; e.currentTarget.style.background='none'; }}
              >Clear</button>
              <button style={S.closeBtn} onClick={handleToggle} title="Close"
                onMouseEnter={e => e.currentTarget.style.background='rgba(255,255,255,0.13)'}
                onMouseLeave={e => e.currentTarget.style.background='rgba(255,255,255,0.06)'}
              >
                <svg width="11" height="11" viewBox="0 0 11 11" fill="none">
                  <path d="M1.5 1.5l8 8M9.5 1.5l-8 8" stroke="#8b949e" strokeWidth="1.6" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
          </div>

          {/* Messages */}
          <div style={S.messages} ref={msgsRef}>
            {messages.map(msg => (
              <div key={msg.id} style={S.bubbleWrap(msg.role === 'user')}>
                <div>
                  {msg.role === 'assistant' && <div style={S.botLabel}>Finance Assistant</div>}
                  <div className="chat-bubble" style={S.bubble(msg.role === 'user')}
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }} />
                </div>
              </div>
            ))}
            {loading && (
              <div style={S.bubbleWrap(false)}>
                <div>
                  <div style={S.botLabel}>Finance Assistant</div>
                  <div style={S.typingWrap}>
                    {[0,1,2].map(i => <span key={i} style={S.typingDot(i)} />)}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* FAQ chips */}
          <div style={S.faqRow}>
            {MINI_FAQS.slice(0, 4).map(faq => (
              <button key={faq.label} style={S.faqChip}
                onClick={() => sendMessage(faq.query)} disabled={loading}
                onMouseEnter={e => { e.currentTarget.style.background='rgba(37,99,235,0.2)'; e.currentTarget.style.borderColor='rgba(37,99,235,0.45)'; }}
                onMouseLeave={e => { e.currentTarget.style.background='rgba(37,99,235,0.1)'; e.currentTarget.style.borderColor='rgba(37,99,235,0.22)'; }}
              >{faq.label}</button>
            ))}
          </div>

          {/* Input bar — textarea + send side by side, no overlap */}
          <div style={S.inputBar}>
            <textarea ref={textareaRef} style={S.textarea} value={input}
              onChange={handleInput} onKeyDown={handleKeyDown}
              placeholder="Ask about EMI, loans, interest..." rows={1} disabled={loading}
              onFocus={e => e.target.style.borderColor='rgba(59,130,246,0.45)'}
              onBlur={e => e.target.style.borderColor='rgba(255,255,255,0.1)'}
            />
            <button style={S.sendBtn(canSend)} onClick={() => sendMessage()} disabled={!canSend} title="Send (Enter)">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M14 8L2 2l2.5 6L2 14l12-6z" fill="currentColor" stroke="currentColor" strokeWidth="0.3" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>

          <div style={S.footer}>Powered by Groq · Built-in rules</div>
        </div>
      )}

      {/* FAB — renders last = top paint order = never covered */}
      <button style={S.fab(open)} onClick={handleToggle}
        title={open ? 'Close' : 'Finance Assistant'} aria-label="Finance assistant"
        onMouseEnter={e => e.currentTarget.style.transform='scale(1.08)'}
        onMouseLeave={e => e.currentTarget.style.transform='scale(1)'}
      >
        {open ? (
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M4 4l10 10M14 4L4 14" stroke="white" strokeWidth="2.2" strokeLinecap="round"/>
          </svg>
        ) : (
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
            <path d="M3 6a2 2 0 012-2h12a2 2 0 012 2v8a2 2 0 01-2 2H7l-4 3V6z" fill="white" fillOpacity="0.95"/>
            <circle cx="8"  cy="10" r="1.2" fill="#1d4ed8"/>
            <circle cx="11" cy="10" r="1.2" fill="#1d4ed8"/>
            <circle cx="14" cy="10" r="1.2" fill="#1d4ed8"/>
          </svg>
        )}
        {showBadge && !open && <span style={S.badge} />}
      </button>
    </>
  );
}
