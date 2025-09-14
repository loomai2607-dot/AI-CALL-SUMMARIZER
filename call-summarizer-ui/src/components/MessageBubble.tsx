
import React from 'react';

const MessageBubble = ({ role, content }: { role: string; content: string }) => (
  <div
  style={{
    margin: '0.5rem 0',
    alignSelf: role === 'user' ? 'flex-end' : 'flex-start',
    background: role === 'user' ? '#DCF8C6' : '#F1F0F0',
    padding: '0.75rem 1rem',
    borderRadius: '1rem',
    maxWidth: '70%',
    wordBreak: 'break-word',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
  }}
>

    {content}
  </div>
);

export default MessageBubble;
