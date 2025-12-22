import React from 'react';
import Chatbot from './Chatbot/Chatbot';

// Safe wrapper for the Chatbot component to prevent errors from breaking the UI
const SafeChatbot = () => {
  try {
    return <Chatbot />;
  } catch (error) {
    console.error("Chatbot error:", error);
    // Simple fallback button in case of error
    return (
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 99999,
          backgroundColor: '#3498db',
          color: 'white',
          border: 'none',
          borderRadius: '50px',
          padding: '15px 20px',
          fontSize: '16px',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
        }}
      >
        🤖 AI Assistant
      </div>
    );
  }
};

export default SafeChatbot;