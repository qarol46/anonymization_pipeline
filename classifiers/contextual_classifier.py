"""Rule-based классификатор для различения типов сущностей"""

import re
from config.settings import INTERNAL_ORG_KEYWORDS, EXTERNAL_ORG_KEYWORDS

class ContextualClassifier:
    """Классифицирует сущности на основе контекста"""
    
    def __init__(self, context_window: int = 100):
        """
        Args:
            context_window: Размер окна контекста вокруг сущности (в символах)
        """
        self.context_window = context_window
    
    def _get_context(self, text: str, start: int, end: int) -> str:
        """Извлекает контекст вокруг сущности"""
        ctx_start = max(0, start - self.context_window)
        ctx_end = min(len(text), end + self.context_window)
        return text[ctx_start:ctx_end].lower()
    
    def classify_organization(self, text: str, start: int, end: int) -> str:
        """
        Классифицирует организацию как внутреннюю или внешнюю
        
        Returns:
            "INTERNAL_ORG" или "EXTERNAL_ORG"
        """
        context = self._get_context(text, start, end)
        
        # Подсчитываем совпадения с ключевыми словами
        internal_score = sum(1 for kw in INTERNAL_ORG_KEYWORDS if kw in context)
        external_score = sum(1 for kw in EXTERNAL_ORG_KEYWORDS if kw in context)
        
        # Если есть явные признаки внутренней организации
        if internal_score > external_score:
            return "INTERNAL_ORG"
        
        # Если есть явные признаки внешней организации
        if external_score > internal_score:
            return "EXTERNAL_ORG"
        
        # По умолчанию считаем внешней (более безопасное решение)
        return "EXTERNAL_ORG"
    
    def classify_location(self, text: str, start: int, end: int) -> str:
        """
        Классифицирует локацию как адрес объекта или регион
        
        Returns:
            "SITE" (адрес объекта) или "REGION" (регион/округ)
        """
        context = self._get_context(text, start, end)
        
        # Ключевые слова для адресов объектов
        site_keywords = ["магазин", "рц", "склад", "офис", "адрес", "улица", "дом"]
        region_keywords = ["регион", "область", "край", "округ", "город", "москва", "санкт-петербург"]
        
        site_score = sum(1 for kw in site_keywords if kw in context)
        region_score = sum(1 for kw in region_keywords if kw in context)
        
        if region_score > site_score:
            return "REGION"
        
        return "SITE"