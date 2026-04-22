import React from 'react';

export default function TypingIndicator() {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      padding: '12px 16px',
      background: 'var(--bg-card)',
      borderRadius: '18px 18px 18px 4px',
      width: 'fit-content',
      border: '1px solid var(--border)',
    }}>
      {[0, 1, 2].map(i => (
        <span key={i} style={{
          width: '7px',
          height: '7px',
          borderRadius: '50%',
          background: 'var(--tata-blue-light)',
          display: 'inline-block',
          animation: `typing-dot 1.2s ease-in-out infinite`,
          animationDelay: `${i * 0.2}s`,
        }} />
      ))}
    </div>
  );
}
