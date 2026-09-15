"""Распознаватель российских документов (СНИЛС, ИНН, паспорта)"""

from presidio_analyzer import PatternRecognizer, Pattern

class RussianDocsRecognizer:
    """Возвращает список распознавателей для российских документов"""
    
    @staticmethod
    def get_recognizers():
        patterns = [
            Pattern("SNILS", r"\d{3}-\d{3}-\d{3}\s\d{2}", 0.9),
            Pattern("INN_PERSON", r"\b\d{12}\b", 0.7),
            Pattern("INN_ORG", r"\b\d{10}\b", 0.6),
            Pattern("RU_PASSPORT", r"\d{4}\s\d{6}", 0.8),
        ]
        
        return [
            PatternRecognizer(
                supported_entity="ID_CARD",
                patterns=patterns,
                supported_language="ru"
            )
        ]