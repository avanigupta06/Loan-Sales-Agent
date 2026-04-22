import React from 'react';
import { renderMarkdown } from '../utils/markdown';

const AGENT_LABELS = {
  master: { label: 'Digital Sales Assistant', color: '#2456a4' },
  sales: { label: 'Digital Sales Assistant · Sales', color: '#2456a4' },
  verification: { label: 'KYC Verification Agent', color: '#7c3aed' },
  underwriting: { label: 'Underwriting Agent', color: '#b45309' },
  sanction: { label: 'Sanction Agent', color: '#065f46' },
};

export default function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';
  const agent = AGENT_LABELS[msg.agent] || AGENT_LABELS.master;

  return (
    <div style={{
      display: 'flex',
      flexDirection: isUser ? 'row-reverse' : 'row',
      alignItems: 'flex-end',
      gap: '10px',
      animation: 'fadeUp 0.3s ease-out both',
      padding: '2px 0',
    }}>
      {/* Avatar */}
      {!isUser && (
        <div style={{
          width: '34px',
          height: '34px',
          borderRadius: '50%',
          background: `linear-gradient(135deg, ${agent.color}, #1a3c6e)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '14px',
          flexShrink: 0,
          border: '2px solid rgba(255,255,255,0.1)',
        }}>
          🤖
        </div>
      )}

      <div style={{ maxWidth: '75%', display: 'flex', flexDirection: 'column',
        alignItems: isUser ? 'flex-end' : 'flex-start' }}>
        {/* Agent label */}
        {!isUser && (
          <span style={{
            fontSize: '11px',
            color: agent.color,
            fontWeight: 600,
            marginBottom: '4px',
            letterSpacing: '0.3px',
          }}>
            {agent.label}
          </span>
        )}

        {/* Bubble */}
        <div
          className="chat-bubble"
          style={{
            padding: '12px 16px',
            borderRadius: isUser
              ? '18px 18px 4px 18px'
              : '18px 18px 18px 4px',
            background: isUser
              ? 'linear-gradient(135deg, #2456a4, #1a3c6e)'
              : 'var(--bg-card)',
            border: isUser
              ? '1px solid rgba(74,127,212,0.3)'
              : '1px solid var(--border)',
            color: 'var(--text-primary)',
            fontSize: '14px',
            lineHeight: '1.65',
            boxShadow: isUser
              ? '0 4px 16px rgba(36,86,164,0.3)'
              : '0 2px 8px rgba(0,0,0,0.2)',
          }}
          dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
        />

        {/* Timestamp */}
        <span style={{
          fontSize: '10px',
          color: 'var(--text-muted)',
          marginTop: '3px',
        }}>
          {msg.time}
        </span>
      </div>
    </div>
  );
}
