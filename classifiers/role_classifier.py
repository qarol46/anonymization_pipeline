"""Классификатор ролей (руководитель-подчинённый)"""

import re
from config.settings import ROLE_KEYWORDS

class RoleClassifier:
    """Определяет роли сотрудников на основе контекста"""
    
    def __init__(self, context_window: int = 150):
        self.context_window = context_window
    
    def _get_context(self, text: str, start: int, end: int) -> str:
        """Извлекает контекст вокруг сущности"""
        ctx_start = max(0, start - self.context_window)
        ctx_end = min(len(text), end + self.context_window)
        return text[ctx_start:ctx_end].lower()
    
    def classify_person_role(self, text: str, start: int, end: int) -> dict:
        """
        Определяет роль персоны
        
        Returns:
            dict с ключами:
            - "role": "supervisor" | "subordinate" | "responsible" | "unknown"
            - "confidence": float (0.0 - 1.0)
            - "evidence": list[str] (найденные ключевые слова)
        """
        context = self._get_context(text, start, end)
        
        scores = {}
        evidence = {}
        
        for role, keywords in ROLE_KEYWORDS.items():
            matches = [kw for kw in keywords if kw in context]
            scores[role] = len(matches)
            evidence[role] = matches
        
        # Находим роль с максимальным score
        if max(scores.values()) == 0:
            return {"role": "unknown", "confidence": 0.0, "evidence": []}
        
        best_role = max(scores, key=scores.get)
        total_keywords = sum(scores.values())
        confidence = scores[best_role] / total_keywords if total_keywords > 0 else 0.0
        
        return {
            "role": best_role,
            "confidence": confidence,
            "evidence": evidence[best_role]
        }
    
    def extract_hierarchy(self, text: str) -> list:
        """
        Извлекает иерархические связи из текста
        
        Returns:
            list of dicts: [{"supervisor": "PERSON_1", "subordinate": "PERSON_2", "context": "..."}]
        """
        hierarchies = []
        
        # Паттерны для поиска связей
        patterns = [
            r"(?P<supervisor>PERSON_\d+)\s+(?:и|,)\s+(?P<subordinate>PERSON_\d+)",
            r"(?P<supervisor>PERSON_\d+)\s+(?:руководит|курирует|контролирует)\s+(?P<subordinate>PERSON_\d+)",
            r"(?P<subordinate>PERSON_\d+)\s+(?:подчиняется|отчитывается перед)\s+(?P<supervisor>PERSON_\d+)",
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                hierarchies.append({
                    "supervisor": match.group("supervisor"),
                    "subordinate": match.group("subordinate"),
                    "context": text[max(0, match.start() - 50):min(len(text), match.end() + 50)]
                })
        
        return hierarchies