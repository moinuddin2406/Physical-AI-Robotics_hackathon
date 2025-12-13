"""
Translation service for the textbook, including Urdu translation capability
"""
from typing import Optional
import googletrans
from googletrans import Translator


class TranslationService:
    """
    Service for translating textbook content and responses
    """
    
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'en': 'English',
            'ur': 'Urdu',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Translate text to the target language
        """
        if target_language not in self.supported_languages:
            raise ValueError(f"Language '{target_language}' is not supported")
        
        if target_language == source_language:
            return text
        
        try:
            # For Urdu (or other right-to-left languages), we might need special handling
            result = self.translator.translate(text, src=source_language, dest=target_language)
            return result.text
        except Exception as e:
            # In case of translation failure, return original text with warning
            return f"[TRANSLATION ERROR: {str(e)}] {text}"
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported
        """
        return language_code in self.supported_languages


# For now, using a mock implementation since googletrans can be unreliable
# In a production system, you might use a more robust translation service
class MockTranslationService:
    """
    Mock translation service for demonstration purposes
    For Urdu translation, we'll return the English text with a note
    """
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'ur': 'Urdu'
        }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Mock translation - returns original text or placeholder for unsupported translations
        """
        if target_language == 'ur':
            # For demo purposes, return the English text with an indication that it would be translated
            return f"[URDU TRANSLATION: {text}]"
        elif target_language == source_language:
            return text
        else:
            # For other languages, return the same text with language tag
            return f"[TRANSLATION TO {target_language.upper()}: {text}]"
    
    def is_language_supported(self, language_code: str) -> bool:
        """
        Check if a language is supported
        """
        return language_code in self.supported_languages