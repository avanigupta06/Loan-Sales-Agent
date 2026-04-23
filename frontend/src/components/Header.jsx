import React, { useState } from 'react';

const STAGES = {
  greeting:         { label: 'Welcome',             color: '#64748b', bg: 'rgba(100,116,139,0.1)',  dot: '#64748b', icon: '👋' },
  collect_phone:    { label: 'Phone Verification',  color: '#3b82f6', bg: 'rgba(59,130,246,0.1)',   dot: '#3b82f6', icon: '📱' },
  auth:             { label: 'Identity Check',       color: '#8b5cf6', bg: 'rgba(139,92,246,0.1)',   dot: '#8b5cf6', icon: '🔐' },
  sales:            { label: 'Loan Requirements',   color: '#f59e0b', bg: 'rgba(245,158,11,0.1)',   dot: '#f59e0b', icon: '💼' },
  verification:     { label: 'KYC Verification',    color: '#a78bfa', bg: 'rgba(167,139,250,0.1)',   dot: '#a78bfa', icon: '🪪' },
  underwriting:     { label: 'Credit Assessment',   color: '#f97316', bg: 'rgba(249,115,22,0.1)',   dot: '#f97316', icon: '📊' },
  salary_upload:    { label: 'Income Verification', color: '#ec4899', bg: 'rgba(236,72,153,0.1)',   dot: '#ec4899', icon: '📎' },
  sanction_confirm: { label: 'Sanction Consent',    color: '#10b981', bg: 'rgba(16,185,129,0.1)',   dot: '#10b981', icon: '✅' },
  decision:         { label: 'Final Decision',      color: '#10b981', bg: 'rgba(16,185,129,0.1)',   dot: '#10b981', icon: '⚖️'  },
  complete:         { label: 'Complete',             color: '#10b981', bg: 'rgba(16,185,129,0.1)',   dot: '#10b981', icon: '🎊' },
};

const STAGE_ORDER = [
  'collect_phone', 'auth', 'sales', 'verification',
  'underwriting', 'salary_upload', 'sanction_confirm', 'complete',
];

export default function Header({ stage, onNewChat }) {
  const info = STAGES[stage] || STAGES.greeting;
  const [hoverBtn, setHoverBtn] = useState(false);

  const currentIdx = STAGE_ORDER.indexOf(stage);

  return (
    <header className="app-header">
      {/* ── Left: Logo + Brand ───────────────────────────── */}
      <div className="header-brand">
        <div className="header-logo">
          <span className="header-logo-icon">🤖</span>
        </div>
        <div className="header-brand-text">
          <span className="header-title">Loan Sale Agentic AI</span>
          <span className="header-subtitle">Digital Sales Assistant · Personal Loans</span>
        </div>
      </div>

      {/* ── Centre: Progress bar + Stage pill ───────────── */}
      <div className="header-centre">
        {/* Mini progress track */}
        <div className="header-progress-track">
          {STAGE_ORDER.map((s, i) => (
            <div
              key={s}
              className={`header-progress-dot ${
                i < currentIdx ? 'done' :
                i === currentIdx ? 'active' : 'pending'
              }`}
              style={i === currentIdx ? { background: info.dot, boxShadow: `0 0 0 3px ${info.dot}30` } : {}}
            />
          ))}
        </div>

        {/* Stage pill */}
        <div className="header-stage-pill" style={{ background: info.bg }}>
          <span className="header-stage-dot" style={{ background: info.dot }} />
          <span className="header-stage-label" style={{ color: info.color }}>
            {info.label}
          </span>
        </div>
      </div>

      {/* ── Right: Actions ───────────────────────────────── */}
      <div className="header-actions">
        <button
          className="header-btn-new"
          onClick={onNewChat}
          onMouseEnter={() => setHoverBtn(true)}
          onMouseLeave={() => setHoverBtn(false)}
        >
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 1v12M1 7h12" stroke="currentColor" strokeWidth="1.8"
              strokeLinecap="round"/>
          </svg>
          New Chat
        </button>
      </div>
    </header>
  );
}
