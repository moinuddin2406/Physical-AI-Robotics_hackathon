import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    
    // Simulate bot response
    setTimeout(() => {
      const botMessage = { 
        id: Date.now() + 1, 
        text: "Thanks for your question! This is a placeholder response. The actual chatbot will connect to the RAG backend to answer questions about the textbook content.", 
        sender: 'bot' 
      };
      setMessages(prev => [...prev, botMessage]);
    }, 500);

    setInputValue('');
  };

  return (
    <div className="chatbot-container">
      {/* Chatbot toggle button */}
      <div className="chatbot-toggle" onClick={toggleChatbot}>
        <span>🤖 AI Assistant</span>
      </div>

      {/* Chatbot panel */}
      {isOpen && (
        <div className="chatbot-panel">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button className="chatbot-close" onClick={toggleChatbot}>×</button>
          </div>
          
          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your book assistant. Ask me anything about the content you're reading.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div 
                  key={message.id} 
                  className={`chatbot-message ${message.sender}-message`}
                >
                  {message.text}
                </div>
              ))
            )}
          </div>
          
          <form className="chatbot-input-form" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask a question about the book..."
            />
            <button type="submit">Send</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;