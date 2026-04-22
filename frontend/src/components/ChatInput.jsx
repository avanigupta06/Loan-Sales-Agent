import React, { useState, useRef } from 'react';

export default function ChatInput({ onSend, disabled, placeholder }) {
  const [value, setValue] = useState('');
  const textareaRef = useRef();

  const handleSend = () => {
    const msg = value.trim();
    if (!msg || disabled) return;
    onSend(msg);
    setValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e) => {
    setValue(e.target.value);
    // Auto-resize
    const ta = e.target;
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 120) + 'px';
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'flex-end',
      gap: '10px',
      padding: '14px 20px',
      background: 'var(--bg-secondary)',
      borderTop: '1px solid var(--border)',
    }}>
      <div style={{
        flex: 1,
        display: 'flex',
        alignItems: 'flex-end',
        background: 'var(--bg-input)',
        border: '1px solid var(--border)',
        borderRadius: '14px',
        padding: '10px 14px',
        transition: 'border-color 0.2s',
      }}
        onFocus={() => {}}
      >
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={placeholder || 'Type your message...'}
          rows={1}
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            outline: 'none',
            color: 'var(--text-primary)',
            fontSize: '14px',
            fontFamily: 'inherit',
            resize: 'none',
            lineHeight: '1.5',
            maxHeight: '120px',
            overflowY: 'auto',
          }}
        />
      </div>

      <button
        onClick={handleSend}
        disabled={disabled || !value.trim()}
        style={{
          width: '44px',
          height: '44px',
          borderRadius: '12px',
          background: disabled || !value.trim()
            ? 'var(--bg-input)'
            : 'linear-gradient(135deg, #2456a4, #1a3c6e)',
          border: '1px solid var(--border)',
          color: disabled || !value.trim() ? 'var(--text-muted)' : 'white',
          cursor: disabled || !value.trim() ? 'not-allowed' : 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '18px',
          flexShrink: 0,
          transition: 'all 0.2s ease',
          boxShadow: disabled || !value.trim() ? 'none' : '0 4px 12px rgba(36,86,164,0.4)',
        }}
      >
        ➤
      </button>
    </div>
  );
}
