"""Главный скрипт запуска пайплайна"""

import os
import json
from datetime import datetime
from processors.text_processor import TextProcessor
from processors.filename_processor import FilenameProcessor
from validators.post_check import PostAnonymizationValidator
from config.settings import INPUT_DIR, OUTPUT_DIR, LOG_FILE

def main():
    print("=" * 60)
    print("ПИПАЛАЙН АНОНИМИЗАЦИИ")
    print("=" * 60)
    
    # 1. Инициализация
    print("\n[1/4] Инициализация компонентов...")
    text_processor = TextProcessor()
    filename_processor = FilenameProcessor(text_processor.pseudonymizer)
    validator = PostAnonymizationValidator()
    
    # 2. Обработка корпуса
    print(f"\n[2/4] Обработка корпуса из {INPUT_DIR}...")
    text_processor.process_corpus(INPUT_DIR, OUTPUT_DIR)
    
    # 3. Обработка имен файлов
    print("\n[3/4] Обработка имен файлов...")
    files = os.listdir(OUTPUT_DIR)
    for filename in files:
        new_filename = filename_processor.process_filename(filename)
        if new_filename != filename:
            old_path = os.path.join(OUTPUT_DIR, filename)
            new_path = os.path.join(OUTPUT_DIR, new_filename)
            os.rename(old_path, new_path)
            print(f"  Переименован: {filename} → {new_filename}")
    
    # 4. Валидация
    print("\n[4/4] Контрольная проверка...")
    validation_result = validator.validate_corpus(OUTPUT_DIR)
    
    if validation_result.passed:
        print("Все проверки пройдены!")
    else:
        print("Обнаружены проблемы:")
        for issue in validation_result.issues[:10]:
            print(f"  - {issue}")
        if len(validation_result.issues) > 10:
            print(f"  ... и еще {len(validation_result.issues) - 10} проблем")
    
    # 5. Сохранение протокола
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "input_dir": INPUT_DIR,
        "output_dir": OUTPUT_DIR,
        "files_processed": len(files),
        "validation_passed": validation_result.passed,
        "validation_issues": validation_result.issues,
        "entity_counts": dict(text_processor.pseudonymizer.counters),
        "total_placeholders": len(text_processor.pseudonymizer.type_map)
    }
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nПротокол сохранен в {LOG_FILE}")
    print("=" * 60)

if __name__ == "__main__":
    main()