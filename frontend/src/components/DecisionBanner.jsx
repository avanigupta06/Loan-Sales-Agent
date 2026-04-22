import React from 'react';

export default function DecisionBanner({ decision, sessionId }) {
  if (!decision) return null;

  const approved = decision === 'approved';

  return (
    <div style={{
      margin: '8px 0',
      padding: '16px 20px',
      borderRadius: '16px',
      background: approved
        ? 'linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.08))'
        : 'linear-gradient(135deg, rgba(239,68,68,0.12), rgba(185,28,28,0.08))',
      border: `1px solid ${approved ? 'rgba(16,185,129,0.3)' : 'rgba(239,68,68,0.3)'}`,
      animation: 'fadeUp 0.5s ease-out',
      textAlign: 'center',
    }}>
      <div style={{ fontSize: '32px', marginBottom: '8px' }}>
        {approved ? '🎉' : '😔'}
      </div>
      <div style={{
        fontFamily: 'Syne, sans-serif',
        fontWeight: 800,
        fontSize: '18px',
        color: approved ? '#34d399' : '#f87171',
        letterSpacing: '-0.3px',
        marginBottom: '6px',
      }}>
        Loan {approved ? 'APPROVED' : 'REJECTED'}
      </div>

      {approved && sessionId && (
        <a
          href={`http://localhost:8000/generate-pdf/${sessionId}`}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            marginTop: '10px',
            padding: '10px 20px',
            background: 'linear-gradient(135deg, #059669, #10b981)',
            color: 'white',
            borderRadius: '10px',
            fontSize: '13px',
            fontWeight: 700,
            textDecoration: 'none',
            boxShadow: '0 4px 16px rgba(16,185,129,0.3)',
            transition: 'opacity 0.2s',
          }}
          onMouseEnter={e => e.currentTarget.style.opacity = '0.9'}
          onMouseLeave={e => e.currentTarget.style.opacity = '1'}
        >
          📄 Download Sanction Letter (PDF)
        </a>
      )}

      {!approved && (
        <p style={{
          fontSize: '12px',
          color: 'rgba(248,113,113,0.8)',
          marginTop: '6px',
        }}>
          Contact us at 1800-267-6060 for assistance
        </p>
      )}
    </div>
  );
}
