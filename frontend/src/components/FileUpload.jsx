import React, { useRef, useState } from 'react';

export default function FileUpload({ onUpload, isUploading }) {
  const inputRef = useRef();
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFile = (file) => {
    if (!file) return;
    const allowed = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
    if (!allowed.includes(file.type)) {
      alert('Please upload a PDF or image file.');
      return;
    }
    setSelectedFile(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleSubmit = () => {
    if (selectedFile) {
      onUpload(selectedFile);
      setSelectedFile(null);
    }
  };

  return (
    <div style={{
      background: 'var(--bg-card)',
      border: '1px solid var(--border)',
      borderRadius: '16px',
      padding: '20px',
      margin: '8px 0',
    }}>
      <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '12px', fontWeight: 500 }}>
        📎 Upload Salary Slip (PDF or Image)
      </p>

      {/* Drop zone */}
      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        style={{
          border: `2px dashed ${dragOver ? 'var(--tata-blue-light)' : 'var(--border)'}`,
          borderRadius: '12px',
          padding: '24px',
          textAlign: 'center',
          cursor: 'pointer',
          background: dragOver ? 'rgba(74,127,212,0.08)' : 'var(--bg-input)',
          transition: 'all 0.2s ease',
        }}
      >
        <div style={{ fontSize: '28px', marginBottom: '8px' }}>
          {selectedFile ? '📄' : '☁️'}
        </div>
        <p style={{ fontSize: '13px', color: selectedFile ? 'var(--accent-green)' : 'var(--text-secondary)' }}>
          {selectedFile
            ? `✓ ${selectedFile.name}`
            : 'Click or drag & drop your salary slip here'}
        </p>
        {!selectedFile && (
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Supported: PDF, JPG, PNG
          </p>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.jpg,.jpeg,.png"
        style={{ display: 'none' }}
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {selectedFile && (
        <button
          onClick={handleSubmit}
          disabled={isUploading}
          style={{
            marginTop: '12px',
            width: '100%',
            padding: '11px',
            background: isUploading
              ? 'var(--bg-input)'
              : 'linear-gradient(135deg, #2456a4, #1a3c6e)',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            fontSize: '14px',
            fontWeight: 600,
            cursor: isUploading ? 'not-allowed' : 'pointer',
            fontFamily: 'inherit',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            transition: 'opacity 0.2s',
          }}
        >
          {isUploading ? (
            <>
              <span style={{
                width: '14px', height: '14px',
                border: '2px solid rgba(255,255,255,0.3)',
                borderTopColor: 'white',
                borderRadius: '50%',
                animation: 'spin 0.8s linear infinite',
                display: 'inline-block',
              }} />
              Uploading...
            </>
          ) : '📤 Submit Salary Slip'}
        </button>
      )}
    </div>
  );
}
