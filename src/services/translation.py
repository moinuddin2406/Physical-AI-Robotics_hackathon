"""
Translation service for the textbook, including Urdu translation capability
"""
from typing import Optional


# For now, using a mock implementation since we don't want to add external dependencies
# In a production system, you might use a more robust translation service like Google Translate API
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