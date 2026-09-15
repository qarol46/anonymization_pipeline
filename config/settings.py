"""Конфигурация и константы для пайплайна анонимизации"""

# Типы сущностей и их обработка
ENTITY_RULES = {
    # Обезличиваемые сущности
    "PERSON": {"action": "anonymize", "placeholder": "PERSON"},
    "PHONE_NUMBER": {"action": "anonymize", "placeholder": "CONTACT"},
    "EMAIL_ADDRESS": {"action": "anonymize", "placeholder": "CONTACT"},
    "LOCATION": {"action": "anonymize", "placeholder": "SITE"},
    "ID_CARD": {"action": "anonymize", "placeholder": "CONTACT"},
    "CREDIT_CARD": {"action": "anonymize", "placeholder": "CONTACT"},
    "IP_ADDRESS": {"action": "anonymize", "placeholder": "CONTACT"},
    "URL": {"action": "anonymize", "placeholder": "CONTACT"},
    
    # Сохраняемые сущности
    "DATE_TIME": {"action": "keep"},
    "ORGANIZATION": {"action": "classify"},  # Требуется классификация
    "JOB_TITLE": {"action": "keep"},
}

# Ключевые слова для классификации организаций
INTERNAL_ORG_KEYWORDS = [
    "департамент", "отдел", "служба", "дирекция", "управление",
    "центр", "комитет", "комиссия", "совет", "коллегия",
    "подразделение", "филиал", "представительство", "офис",
    "склад", "магазин", "рц", "распределительный центр"
]

EXTERNAL_ORG_KEYWORDS = [
    "поставщик", "подрядчик", "перевозчик", "исполнитель",
    "заказчик", "клиент", "партнёр", "контрагент", "вендор",
    "компания", "корпорация", "фирма", "предприятие"
]

# Ключевые слова для определения ролей
ROLE_KEYWORDS = {
    "supervisor": ["руководитель", "начальник", "директор", "управляющий", "лидер"],
    "subordinate": ["сотрудник", "специалист", "менеджер", "исполнитель", "работник"],
    "responsible": ["ответственный", "курирует", "контролирует", "отвечает"],
}

# Паттерны для поиска остаточных ФИО
FIO_PATTERNS = [
    r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.\s*[А-ЯЁ]\.",  # Иванов И. И.
    r"[А-ЯЁ]\.\s*[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+",  # И. И. Иванов
    r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\.[А-ЯЁ]\.",     # Иванов И.И.
    r"[А-ЯЁ]\.[А-ЯЁ]\.\s+[А-ЯЁ][а-яё]+",     # И.И. Иванов
    r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+",  # Иванов Иван Иванович
]

# Пути
INPUT_DIR = "input_corpus"
OUTPUT_DIR = "output/anonymized_corpus"
MAPPING_FILE = "output/entity_mapping.json"
LOG_FILE = "output/processing_log.json"