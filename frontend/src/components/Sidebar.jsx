import React from 'react';

export default function Sidebar({ loanStatus, sessionId }) {
  // Demo customer panel has been removed.
  // Users must manually enter their details via chat.

  return (
    <div style={{
      width: '220px',
      minWidth: '220px',
      background: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      padding: '20px 14px',
      gap: '16px',
    }}>
      {/* Brand mark */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(36,86,164,0.15), rgba(36,86,164,0.05))',
        border: '1px solid rgba(36,86,164,0.25)',
        borderRadius: '12px',
        padding: '14px',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '28px', marginBottom: '6px' }}>🤖</div>
        <div style={{ fontSize: '11px', fontWeight: 700, color: '#60a5fa', letterSpacing: '0.3px' }}>
          DIGITAL SALES
        </div>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
          ASSISTANT
        </div>
      </div>

      {/* Loan Status Card */}
      {loanStatus && (
        <div style={{
          background: loanStatus === 'approved'
            ? 'linear-gradient(135deg, #064e3b, #065f46)'
            : 'linear-gradient(135deg, #7f1d1d, #991b1b)',
          border: `1px solid ${loanStatus === 'approved' ? '#10b98130' : '#ef444430'}`,
          borderRadius: '12px',
          padding: '14px',
          animation: 'fadeUp 0.4s ease-out',
          textAlign: 'center',
        }}>
          <div style={{ fontSize: '22px', marginBottom: '4px' }}>
            {loanStatus === 'approved' ? '🎉' : '❌'}
          </div>
          <div style={{
            fontWeight: 700, fontSize: '13px',
            color: loanStatus === 'approved' ? '#34d399' : '#f87171',
          }}>
            Loan {loanStatus === 'approved' ? 'APPROVED' : 'REJECTED'}
          </div>
          {loanStatus === 'approved' && sessionId && (
            <a
              href={`http://localhost:8000/generate-pdf/${sessionId}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-block', marginTop: '8px',
                padding: '6px 12px', background: '#10b981',
                color: 'white', borderRadius: '7px',
                fontSize: '11px', fontWeight: 700, textDecoration: 'none',
              }}
            >
              📄 Download PDF
            </a>
          )}
        </div>
      )}

      {/* Process Steps */}
      <div>
        <p style={{
          fontSize: '10px', fontWeight: 700, letterSpacing: '1px',
          color: 'var(--text-muted)', marginBottom: '10px', textTransform: 'uppercase',
        }}>
          Loan Journey
        </p>
        {[
          { icon: '📱', label: 'Enter Mobile Number' },
          { icon: '🔐', label: 'Identity Verification' },
          { icon: '💼', label: 'Loan Requirements' },
          { icon: '🪪', label: 'KYC Check' },
          { icon: '📊', label: 'Credit Assessment' },
          { icon: '✅', label: 'Decision' },
          { icon: '📄', label: 'Sanction Letter' },
        ].map((step, i) => (
          <div key={i} style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '6px 8px', marginBottom: '2px',
            borderRadius: '7px',
            background: 'rgba(255,255,255,0.02)',
          }}>
            <span style={{ fontSize: '13px', width: '20px', textAlign: 'center' }}>{step.icon}</span>
            <span style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>{step.label}</span>
          </div>
        ))}
      </div>

      {/* Underwriting legend */}
      <div style={{
        padding: '10px',
        background: 'var(--bg-card)',
        borderRadius: '8px',
        border: '1px solid var(--border)',
        fontSize: '10px',
        color: 'var(--text-muted)',
        lineHeight: '1.8',
        marginTop: 'auto',
      }}>
        <strong style={{ color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>
          🧠 Underwriting Rules
        </strong>
        Score &lt; 700 → Reject<br />
        Loan ≤ Limit → Approve<br />
        Loan ≤ 2×Limit → Salary Check<br />
        Loan &gt; 2×Limit → Reject<br />
        EMI &gt; 50% Salary → Reject
      </div>
    </div>
  );
}
