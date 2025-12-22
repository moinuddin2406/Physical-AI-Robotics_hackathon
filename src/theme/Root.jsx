import React, { useState, useEffect } from 'react';
import SafeChatbot from '../components/SafeChatbot';

// Root component that wraps the entire application
const Root = ({ children }) => {
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    // Ensure we're on the client side
    setIsClient(true);
  }, []);

  return (
    <>
      {children}
      {isClient && <SafeChatbot />}
    </>
  );
};

export default Root;