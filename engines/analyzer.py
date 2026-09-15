"""Настроенный AnalyzerEngine с кастомными распознавателями"""

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider

from recognizers.russian_fio import RussianFioRecognizer
from recognizers.russian_docs import RussianDocsRecognizer

def create_analyzer() -> AnalyzerEngine:
    """Создает настроенный AnalyzerEngine"""
    
    # 1. Настраиваем NLP-движок
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "ru", "model_name": "ru_core_news_sm"},
            {"lang_code": "en", "model_name": "en_core_web_sm"}
        ],
    }
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    
    # 2. Создаем реестр распознавателей с явным указанием языков
    # ВАЖНО: Указываем supported_languages при создании реестра
    registry = RecognizerRegistry(supported_languages=["ru", "en"])
    
    # Добавляем кастомные распознаватели
    registry.add_recognizer(RussianFioRecognizer())
    
    for recognizer in RussianDocsRecognizer.get_recognizers():
        registry.add_recognizer(recognizer)
    
    # Фильтруем стандартные распознаватели (отключаем DateTime)
    registry.recognizers = [
        r for r in registry.recognizers 
        if r.name != "DateTimeRecognizer"
    ]
    
    # 3. Создаем AnalyzerEngine
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        registry=registry,
        supported_languages=["ru", "en"]
    )
    
    return analyzer