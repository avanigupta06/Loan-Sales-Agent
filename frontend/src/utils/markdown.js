/**
 * Simple markdown renderer — converts bold, italic, bullet lists, line breaks.
 * Returns HTML string.
 */
export function renderMarkdown(text) {
  if (!text) return '';

  return text
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Inline code
    .replace(/`(.+?)`/g, '<code style="background:rgba(255,255,255,0.1);padding:1px 5px;border-radius:3px;font-size:0.9em">$1</code>')
    // Bullet lists
    .replace(/^[•\-]\s+(.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul style="margin:6px 0 6px 18px;list-style:none">$1</ul>')
    // Numbered lists
    .replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>')
    // Line breaks
    .replace(/\n/g, '<br />');
}
