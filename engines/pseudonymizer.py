"""Псевдонимайзер с раздельной типизацией"""

import json
from collections import defaultdict
from config.settings import ENTITY_RULES

class TypedPseudonymizer:
    """Псевдонимайзер с типизацией и классификацией"""
    
    def __init__(self, mapping_file: str = "output/entity_mapping.json"):
        self.mapping_file = mapping_file
        self.mapping = {}              # "Оригинал" → "Плейсхолдер"
        self.counters = defaultdict(int)  # {"PERSON": 1, "EXTORG": 1}
        self.type_map = {}             # "Плейсхолдер" → тип
        self.role_map = {}             # "Плейсхолдер" → роль (для PERSON)
        self._load_mapping()
    
    def _load_mapping(self):
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mapping = data.get("mapping", {})
                self.counters = defaultdict(int, data.get("counters", {}))
                self.type_map = data.get("type_map", {})
                self.role_map = data.get("role_map", {})
        except FileNotFoundError:
            pass
    
    def save_mapping(self):
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump({
                "mapping": self.mapping,
                "counters": dict(self.counters),
                "type_map": self.type_map,
                "role_map": self.role_map
            }, f, ensure_ascii=False, indent=2)
    
    def _should_anonymize(self, entity_type: str) -> bool:
        """Проверяет, нужно ли анонимизировать этот тип"""
        rule = ENTITY_RULES.get(entity_type)
        if not rule:
            return False
        return rule.get("action") == "anonymize"
    
    def _get_placeholder_type(self, entity_type: str, classified_type: str = None) -> str:
        """Возвращает тип плейсхолдера"""
        if classified_type:
            # Используем классифицированный тип
            return classified_type
        
        rule = ENTITY_RULES.get(entity_type)
        if rule:
            return rule.get("placeholder", "UNKNOWN")
        return "UNKNOWN"
    
    def get_pseudonym(self, entity_type: str, original_value: str, 
                      classified_type: str = None, role: str = None) -> str:
        """Возвращает плейсхолдер с учетом классификации"""
        if original_value in self.mapping:
            return self.mapping[original_value]
        
        placeholder_type = self._get_placeholder_type(entity_type, classified_type)
        self.counters[placeholder_type] += 1
        pseudonym = f"{placeholder_type}_{self.counters[placeholder_type]}"
        
        self.mapping[original_value] = pseudonym
        self.type_map[pseudonym] = placeholder_type
        
        if role:
            self.role_map[pseudonym] = role
        
        return pseudonym
    
    def anonymize_text(self, text: str, analyzer_results, 
                       contextual_classifier=None, role_classifier=None) -> str:
        """Анонимизирует текст с учетом классификации"""
        
        to_anonymize = []
        
        for result in analyzer_results:
            entity_type = result.entity_type
            rule = ENTITY_RULES.get(entity_type)
            
            if not rule:
                continue
            
            action = rule.get("action")
            
            if action == "keep":
                # Сохраняем без изменений
                continue
            
            elif action == "classify":
                # Требуется классификация
                if contextual_classifier:
                    if entity_type == "ORGANIZATION":
                        classified = contextual_classifier.classify_organization(
                            text, result.start, result.end
                        )
                        if classified == "INTERNAL_ORG":
                            continue  # Не анонимизируем внутренние
                        to_anonymize.append((result, classified, None))
                    
                    elif entity_type == "LOCATION":
                        classified = contextual_classifier.classify_location(
                            text, result.start, result.end
                        )
                        if classified == "REGION":
                            continue  # Не анонимизируем регионы
                        to_anonymize.append((result, classified, None))
            
            elif action == "anonymize":
                # Определяем роль для PERSON
                role = None
                if entity_type == "PERSON" and role_classifier:
                    role_info = role_classifier.classify_person_role(
                        text, result.start, result.end
                    )
                    role = role_info.get("role")
                
                to_anonymize.append((result, None, role))
        
        # Сортируем с конца
        to_anonymize.sort(key=lambda x: x[0].start, reverse=True)
        
        anonymized = text
        for result, classified_type, role in to_anonymize:
            original = text[result.start:result.end]
            pseudonym = self.get_pseudonym(
                result.entity_type, original, classified_type, role
            )
            
            # Добавляем пробелы вокруг плейсхолдера
            before = anonymized[result.start - 1] if result.start > 0 else " "
            after = anonymized[result.end] if result.end < len(anonymized) else " "
            
            left_pad = "" if before.isspace() else " "
            right_pad = "" if after.isspace() else " "
            
            replacement = f"{left_pad}{pseudonym}{right_pad}"
            anonymized = anonymized[:result.start] + replacement + anonymized[result.end:]
        
        return anonymized