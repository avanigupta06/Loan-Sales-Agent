import React from 'react';

const STAGE_LABELS = {
  greeting:         { label: 'Welcome',             color: '#8b949e', icon: '👋' },
  collect_phone:    { label: 'Phone Verification',  color: '#4a7fd4', icon: '📱' },
  auth:             { label: 'Identity Check',       color: '#a78bfa', icon: '🔐' },
  sales:            { label: 'Loan Requirements',   color: '#f59e0b', icon: '💼' },
  verification:     { label: 'KYC Verification',    color: '#8b5cf6', icon: '🪪' },
  underwriting:     { label: 'Credit Assessment',   color: '#f97316', icon: '📊' },
  salary_upload:    { label: 'Income Verification', color: '#ec4899', icon: '📎' },
  sanction_confirm: { label: 'Sanction Consent',    color: '#10b981', icon: '✅' },
  decision:         { label: 'Final Decision',      color: '#10b981', icon: '⚖️' },
  complete:         { label: 'Complete',             color: '#10b981', icon: '🎊' },
};

export default function Header({ stage, onNewChat }) {
  const stageInfo = STAGE_LABELS[stage] || STAGE_LABELS.greeting;

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '14px 24px',
      background: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border)',
      flexShrink: 0,
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '38px', height: '38px',
          background: 'linear-gradient(135deg, #1a3c6e, #2456a4)',
          borderRadius: '10px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '18px',
          boxShadow: '0 0 20px rgba(36,86,164,0.4)',
        }}>
          🤖
        </div>
        <div>
          <div style={{
            fontFamily: 'Syne, sans-serif',
            fontWeight: 800,
            fontSize: '14px',
            color: 'var(--text-primary)',
            letterSpacing: '-0.3px',
          }}>
            LOAN SALE AGENTIC AI SYSTEM
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-muted)', letterSpacing: '0.5px' }}>
            DIGITAL SALES ASSISTANT · PERSONAL LOANS
          </div>
        </div>
      </div>

      {/* Stage indicator */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: '8px',
        background: 'var(--bg-card)',
        border: '1px solid var(--border)',
        borderRadius: '20px', padding: '5px 12px',
      }}>
        <span>{stageInfo.icon}</span>
        <span style={{
          fontSize: '11px', fontWeight: 600,
          color: stageInfo.color, letterSpacing: '0.3px',
        }}>
          {stageInfo.label}
        </span>
      </div>

      {/* New Chat */}
      <button
        onClick={onNewChat}
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border)',
          color: 'var(--text-secondary)',
          borderRadius: '10px',
          padding: '7px 14px',
          fontSize: '12px',
          cursor: 'pointer',
          fontFamily: 'inherit',
          fontWeight: 600,
          display: 'flex', alignItems: 'center', gap: '6px',
          transition: 'all 0.15s ease',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.borderColor = 'var(--tata-blue-light)';
          e.currentTarget.style.color = 'var(--text-primary)';
        }}
        onMouseLeave={e => {
          e.currentTarget.style.borderColor = 'var(--border)';
          e.currentTarget.style.color = 'var(--text-secondary)';
        }}
      >
        ✦ New Chat
      </button>
    </div>
  );
}
