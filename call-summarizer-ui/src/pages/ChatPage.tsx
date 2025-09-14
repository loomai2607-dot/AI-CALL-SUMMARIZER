import React, { useState } from 'react';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';
import TraceCanvas from '../components/TraceCanvas';

const ChatPage = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [trace, setTrace] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<string>('');
  const [showTrace, setShowTrace] = useState(false);
  const apiUrl=`${import.meta.env.VITE_API_BASE_CALL_SUMMARY_URL}/upload-call`

  const handleNewMessage = (message: any, trace?: any[], recos?: string) => {
    setMessages((prev) => [...prev, message]);
    if (trace) {
      setTrace(trace);
      setShowTrace(true);
    }
    if (recos) {
      setRecommendations(recos);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw' }}>
      <div style={{ padding: '1rem', background: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
        <h2 style={{ margin: 0 }}>📞 AI Call Summarizer</h2>
      </div>
      <div style={{ flex: 1, display: 'flex', overflow: 'auto' }}>
      <div style={{ flex: 2, display: 'flex', flexDirection: 'column', overflowY: 'auto', maxHeight: '100vh' }}>

          <ChatWindow messages={messages} />
          {recommendations && (
            <div style={{ padding: '1rem', background: '#e7f5ff', borderTop: '1px solid #b3d7f5' }}>
              <h4>🔍 Recommendations</h4>
              <p>{recommendations}</p>
            </div>
          )}
          <ChatInput
            onSend={(msg, trace, recos) => handleNewMessage(msg, trace, recos)}
            apiUrl={apiUrl}
          />
        </div>
        {showTrace && (
          <div style={{ width: 400, borderLeft: '1px solid #ccc' }}>
            <TraceCanvas trace={trace} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatPage;