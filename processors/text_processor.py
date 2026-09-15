"""Обработчик текста документов"""

import os
from engines.analyzer import create_analyzer
from engines.pseudonymizer import TypedPseudonymizer
from classifiers.contextual_classifier import ContextualClassifier
from classifiers.role_classifier import RoleClassifier

class TextProcessor:
    """Обрабатывает текст документов"""
    
    def __init__(self):
        self.analyzer = create_analyzer()
        self.pseudonymizer = TypedPseudonymizer()
        self.contextual_classifier = ContextualClassifier()
        self.role_classifier = RoleClassifier()
    
    def process_text(self, text: str, language: str = 'ru') -> str:
        """Обрабатывает один текст"""
        # Анализ
        analyzer_results = self.analyzer.analyze(text=text, language=language)
        
        # Анонимизация с классификацией
        anonymized = self.pseudonymizer.anonymize_text(
            text, analyzer_results,
            contextual_classifier=self.contextual_classifier,
            role_classifier=self.role_classifier
        )
        
        return anonymized
    
    def process_corpus(self, input_dir: str, output_dir: str):
        """Обрабатывает весь корпус"""
        os.makedirs(output_dir, exist_ok=True)
        
        files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
        
        for i, filename in enumerate(files, 1):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            anonymized = self.process_text(text)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(anonymized)
            
            print(f"[{i}/{len(files)}] Обработан: {filename}")
        
        # Сохраняем карту соответствий
        self.pseudonymizer.save_mapping()
        print(f"\nКарта сохранена в {self.pseudonymizer.mapping_file}")