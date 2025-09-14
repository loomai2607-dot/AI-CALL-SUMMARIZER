
import React from 'react';
import MessageBubble from './MessageBubble';

const ChatWindow = ({ messages }: { messages: any[] }) => (
  <div style={{
    flex: 1,
    overflowY: 'auto',
    padding: '1rem',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-end'
  }}>
  
    {messages.map((msg, idx) => (
      <MessageBubble key={idx} role={msg.role} content={msg.content} />
    ))}
  </div>
);

export default ChatWindow;
