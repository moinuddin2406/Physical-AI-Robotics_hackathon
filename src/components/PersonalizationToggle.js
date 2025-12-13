import React, { useState, useEffect } from 'react';
import { usePluginData } from '@docusaurus/useGlobalData';

/**
 * PersonalizationToggle component
 * Allows users to adjust the complexity of explanations
 */
const PersonalizationToggle = ({ onPersonalizationChange }) => {
  const [personalizationEnabled, setPersonalizationEnabled] = useState(false);
  const [complexityLevel, setComplexityLevel] = useState('intermediate');

  useEffect(() => {
    // Load user preferences from localStorage
    const savedPersonalization = localStorage.getItem('personalizationEnabled');
    const savedComplexity = localStorage.getItem('complexityLevel');

    if (savedPersonalization !== null) {
      setPersonalizationEnabled(JSON.parse(savedPersonalization));
    }
    
    if (savedComplexity) {
      setComplexityLevel(savedComplexity);
    }
  }, []);

  useEffect(() => {
    // Save user preferences to localStorage
    localStorage.setItem('personalizationEnabled', JSON.stringify(personalizationEnabled));
    localStorage.setItem('complexityLevel', complexityLevel);

    // Notify parent component of changes
    if (onPersonalizationChange) {
      onPersonalizationChange({
        enabled: personalizationEnabled,
        complexity: complexityLevel
      });
    }
  }, [personalizationEnabled, complexityLevel, onPersonalizationChange]);

  const handleToggle = () => {
    setPersonalizationEnabled(!personalizationEnabled);
  };

  const handleComplexityChange = (e) => {
    setComplexityLevel(e.target.value);
  };

  return (
    <div className="personalization-toggle">
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '10px 0' }}>
        <label style={{ display: 'flex', alignItems: 'center' }}>
          <input
            type="checkbox"
            checked={personalizationEnabled}
            onChange={handleToggle}
            style={{ marginRight: '5px' }}
          />
          <span>Enable Personalization</span>
        </label>
        
        {personalizationEnabled && (
          <select 
            value={complexityLevel} 
            onChange={handleComplexityChange}
            style={{ marginLeft: '10px' }}
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        )}
      </div>
      
      {personalizationEnabled && (
        <div style={{ 
          padding: '10px', 
          backgroundColor: '#f0f8ff', 
          border: '1px solid #b3d9ff', 
          borderRadius: '4px',
          fontSize: '0.9em'
        }}>
          Personalization is enabled. Responses will be adjusted to {complexityLevel} level.
        </div>
      )}
    </div>
  );
};

export default PersonalizationToggle;