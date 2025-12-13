import React, { useState, useEffect } from 'react';

/**
 * LanguageToggle component
 * Allows users to switch between different languages, including Urdu
 */
const LanguageToggle = ({ onLanguageChange }) => {
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [supportedLanguages] = useState({
    'en': 'English',
    'ur': 'Urdu'
  });

  useEffect(() => {
    // Load user language preference from localStorage
    const savedLanguage = localStorage.getItem('selectedLanguage');
    
    if (savedLanguage && supportedLanguages[savedLanguage]) {
      setSelectedLanguage(savedLanguage);
    }
  }, [supportedLanguages]);

  useEffect(() => {
    // Save user language preference to localStorage
    localStorage.setItem('selectedLanguage', selectedLanguage);

    // Notify parent component of language change
    if (onLanguageChange) {
      onLanguageChange(selectedLanguage);
    }
  }, [selectedLanguage, onLanguageChange]);

  const handleLanguageChange = (e) => {
    setSelectedLanguage(e.target.value);
  };

  return (
    <div className="language-toggle">
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px 0' }}>
        <label htmlFor="language-select" style={{ fontWeight: 'bold' }}>
          Language:
        </label>
        <select 
          id="language-select"
          value={selectedLanguage} 
          onChange={handleLanguageChange}
        >
          {Object.entries(supportedLanguages).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>
      
      {selectedLanguage === 'ur' && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#fff2e6', 
          border: '1px solid #ffcc80', 
          borderRadius: '4px',
          fontSize: '0.9em'
        }}>
          Urdu translation mode is active. Responses will be translated to Urdu when possible.
        </div>
      )}
    </div>
  );
};

export default LanguageToggle;