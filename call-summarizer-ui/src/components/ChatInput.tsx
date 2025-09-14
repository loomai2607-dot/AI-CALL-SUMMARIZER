import React, { useState } from 'react';
import axios from 'axios';

const ChatInput = ({ onSend, apiUrl }: { onSend: (msg: any, trace?: any[], recos?: string) => void, apiUrl: string }) => {
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post(apiUrl, formData);
      const { transcript, summary, trace, recommendations } = res.data;

      onSend({ role: 'user', content: file?.name });
      onSend({ role: 'assistant', content: summary }, trace, recommendations);
    } catch (err) {
      console.error(err);
    } finally {
      setText('');
      setFile(null);
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', padding: '1rem', gap: '0.5rem' }}>
      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type your message or upload audio..."
        style={{ flex: 1 }}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
};

export default ChatInput;