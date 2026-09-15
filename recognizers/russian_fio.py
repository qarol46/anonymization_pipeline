"""Распознаватель российских ФИО и ФИО с инициалами"""

from presidio_analyzer import EntityRecognizer, RecognizerResult
import re

class RussianFioRecognizer(EntityRecognizer):
    """Распознает русские ФИО, ФИО с инициалами, Имя Отчество"""
    
    def __init__(self):
        patterns = [
            # Фамилия И.О. или И.О. Фамилия
            r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.",
            r"[А-ЯЁ]\.\s*[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+",
            # Фамилия И.О. (слитно)
            r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\.",
            r"[А-ЯЁ]\.[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+",
            # Полное ФИО (3 слова с заглавной буквы)
            r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+",
            # Имя Отчество (с типовыми суффиксами)
            r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+ич(?:а|у|ем|е)?\b",
            r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+вна\b",
        ]
        self.compiled_patterns = [re.compile(p) for p in patterns]
        super().__init__(supported_entities=["PERSON"], supported_language="ru")

    def load(self) -> None:
        pass

    def analyze(self, text, entities, nlp_artifacts=None):
        results = []
        for pattern in self.compiled_patterns:
            for match in pattern.finditer(text):
                results.append(
                    RecognizerResult(
                        entity_type="PERSON",
                        start=match.start(),
                        end=match.end(),
                        score=0.85
                    )
                )
        return results