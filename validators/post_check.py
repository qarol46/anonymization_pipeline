"""Контрольная проверка после анонимизации"""

import re
import os
from dataclasses import dataclass
from config.settings import FIO_PATTERNS

@dataclass
class ValidationResult:
    passed: bool
    issues: list

class PostAnonymizationValidator:
    """Контрольная проверка по критериям приемки"""
    
    def validate_corpus(self, corpus_dir: str) -> ValidationResult:
        """Проверяет весь корпус"""
        issues = []
        
        files = [f for f in os.listdir(corpus_dir) if f.endswith('.md')]
        
        for filename in files:
            filepath = os.path.join(corpus_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 1. Проверка остаточных ФИО
            for pattern in FIO_PATTERNS:
                matches = re.findall(pattern, text)
                if matches:
                    issues.append(f"{filename}: Найдены остаточные ФИО: {matches[:3]}")
            
            # 2. Проверка контактных данных
            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            if re.search(email_pattern, text):
                issues.append(f"{filename}: Найдены остаточные email")
            
            phone_pattern = r"\+?\d[\d\s\-\(\)]{9,}\d"
            if re.search(phone_pattern, text):
                issues.append(f"{filename}: Найдены остаточные телефоны")
            
            # 3. Проверка склеек
            glue_pattern = r"(PERSON_\d+|EXTORG_\d+|SITE_\d+|CONTACT_\d+)[А-Яа-я]"
            if re.search(glue_pattern, text):
                issues.append(f"{filename}: Найдены склейки плейсхолдеров")
        
        return ValidationResult(passed=len(issues) == 0, issues=issues)