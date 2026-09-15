"""Обработчик имен файлов"""

import os
import re
from config.settings import FIO_PATTERNS

class FilenameProcessor:
    """Обрабатывает имена файлов"""
    
    def __init__(self, pseudonymizer):
        self.pseudonymizer = pseudonymizer
    
    def process_filename(self, filename: str) -> str:
        """Обрабатывает имя файла"""
        name, ext = os.path.splitext(filename)
        
        # Заменяем ФИО на плейсхолдеры
        for pattern in FIO_PATTERNS:
            for match in re.finditer(pattern, name):
                fio = match.group()
                pseudonym = self.pseudonymizer.get_pseudonym("PERSON", fio)
                name = name.replace(fio, f" {pseudonym} ")
        
        # Убираем лишние пробелы
        name = re.sub(r"\s+", " ", name).strip()
        
        return f"{name}{ext}"