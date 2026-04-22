import React, { useState, useEffect, useRef, useCallback } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MessageBubble from './components/MessageBubble';
import TypingIndicator from './components/TypingIndicator';
import ChatInput from './components/ChatInput';
import FileUpload from './components/FileUpload';
import DecisionBanner from './components/DecisionBanner';
import { api } from './utils/api';

function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function App() {
  const [sessionId, setSessionId]       = useState(null);
  const [messages, setMessages]         = useState([]);
  const [stage, setStage]               = useState('greeting');
  const [isTyping, setIsTyping]         = useState(false);
  const [requiresUpload, setRequiresUpload] = useState(false);
  const [isUploading, setIsUploading]   = useState(false);
  const [loanDecision, setLoanDecision] = useState(null);
  const [pdfReady, setPdfReady]         = useState(false);
  const [error, setError]               = useState(null);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(() => { scrollToBottom(); }, [messages, isTyping]);

  const startSession = useCallback(async () => {
    setMessages([]);
    setStage('greeting');
    setIsTyping(true);
    setRequiresUpload(false);
    setLoanDecision(null);
    setPdfReady(false);
    setError(null);

    try {
      const data = await api.newSession();
      setSessionId(data.session_id);
      setIsTyping(false);
      setMessages([{
        id: Date.now(), role: 'assistant',
        content: data.message, agent: data.agent || 'master', time: getTime(),
      }]);
      setStage(data.stage || 'collect_phone');
    } catch {
      setIsTyping(false);
      setError('Cannot connect to backend. Make sure FastAPI is running on port 8000.');
    }
  }, []);

  useEffect(() => { startSession(); }, [startSession]);

  const handleSend = async (userMessage) => {
    if (!sessionId || isTyping) return;
    const userMsg = { id: Date.now(), role: 'user', content: userMessage, agent: null, time: getTime() };
    setMessages(prev => [...prev, userMsg]);
    setIsTyping(true);
    setError(null);

    try {
      await new Promise(r => setTimeout(r, 500 + Math.random() * 500));
      const data = await api.chat(sessionId, userMessage);
      setIsTyping(false);
      setMessages(prev => [...prev, {
        id: Date.now() + 1, role: 'assistant',
        content: data.message, agent: data.agent || 'master', time: getTime(),
      }]);
      setStage(data.stage || stage);
      setRequiresUpload(data.requires_upload || false);
      if (data.loan_decision) setLoanDecision(data.loan_decision);
      if (data.pdf_ready) setPdfReady(true);
    } catch {
      setIsTyping(false);
      setError('Something went wrong. Please try again.');
    }
  };

  const handleUpload = async (file) => {
    if (!sessionId || isUploading) return;
    setIsUploading(true);
    setRequiresUpload(false);
    setError(null);
    setMessages(prev => [...prev, {
      id: Date.now(), role: 'user',
      content: `📎 Uploaded salary slip: **${file.name}**`, agent: null, time: getTime(),
    }]);
    setIsTyping(true);

    try {
      await new Promise(r => setTimeout(r, 1000));
      const data = await api.uploadSalarySlip(sessionId, file);
      setIsTyping(false);
      setIsUploading(false);
      setMessages(prev => [...prev, {
        id: Date.now() + 1, role: 'assistant',
        content: data.message, agent: data.agent || 'underwriting', time: getTime(),
      }]);
      setStage(data.stage || stage);
      setRequiresUpload(data.requires_upload || false);
      if (data.loan_decision) setLoanDecision(data.loan_decision);
      if (data.pdf_ready) setPdfReady(true);
    } catch (err) {
      setIsTyping(false);
      setIsUploading(false);
      setRequiresUpload(true);
      setError(err.message || 'Upload failed. Please try again.');
    }
  };

  const isComplete = stage === 'complete';
  const isSanctionConfirm = stage === 'sanction_confirm';

  const inputPlaceholder = isComplete
    ? 'Session complete — start a New Chat to apply again'
    : requiresUpload
    ? 'Please upload your salary slip above...'
    : isSanctionConfirm
    ? 'Type Yes to proceed or No to decline...'
    : 'Type your message...';

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      {/* Sidebar — no demo customers, just status + journey steps */}
      <Sidebar loanStatus={loanDecision} sessionId={sessionId} />

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Header stage={stage} onNewChat={startSession} />

        {/* Messages */}
        <div style={{
          flex: 1, overflowY: 'auto', padding: '20px 24px',
          display: 'flex', flexDirection: 'column', gap: '10px',
        }}>
          {/* Background glow */}
          <div style={{
            position: 'fixed', top: '10%', right: '5%',
            width: '400px', height: '400px',
            background: 'radial-gradient(circle, rgba(36,86,164,0.06) 0%, transparent 70%)',
            pointerEvents: 'none', zIndex: 0,
          }} />

          {/* Error */}
          {error && (
            <div style={{
              padding: '12px 16px',
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid rgba(239,68,68,0.3)',
              borderRadius: '10px', color: '#f87171', fontSize: '13px',
            }}>
              ⚠️ {error}
            </div>
          )}

          {messages.map(msg => <MessageBubble key={msg.id} msg={msg} />)}

          {/* Typing */}
          {isTyping && (
            <div style={{ animation: 'fadeUp 0.2s ease-out', marginLeft: '44px' }}>
              <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Digital Sales Assistant is typing...
              </div>
              <TypingIndicator />
            </div>
          )}

          {/* Upload */}
          {requiresUpload && !isTyping && (
            <div style={{ animation: 'fadeUp 0.3s ease-out' }}>
              <FileUpload onUpload={handleUpload} isUploading={isUploading} />
            </div>
          )}

          {/* Decision banner */}
          {loanDecision && !isTyping && (
            <DecisionBanner decision={loanDecision} sessionId={sessionId} />
          )}

          <div ref={messagesEndRef} />
        </div>

        <ChatInput
          onSend={handleSend}
          disabled={isTyping || isUploading || (isComplete && !isSanctionConfirm)}
          placeholder={inputPlaceholder}
        />
      </div>
    </div>
  );
}
