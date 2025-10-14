from Final_hw import PreciousMetalsParser, MetalsData
# test_parser.py
import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(__file__))

try:
    # Пробуем импортировать из основного файла (замените 'main' на имя вашего файла)
    from Final_hw import PreciousMetalsParser, MetalsData  # ← ЗАМЕНИТЕ 'main' на имя вашего файла

    print("✅ Импорт успешен!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\n📋 Доступные файлы в директории:")
    for file in Path('.').glob('*.py'):
        print(f"   - {file.name}")
    exit(1)


def test_parser():
    print("🧪 ТЕСТ ПАРСЕРА ЦБ РФ")

    # Тестируем парсер
    parser = PreciousMetalsParser("https://cbr.ru/hd_base/metall/metall_base_new/")
    print("Запускаем парсер...")
    parser.start()

    # Проверяем результат
    file_path = Path('parsed_data') / 'precious_metals.json'
    if file_path.exists():
        print(f"✅ Файл создан: {file_path}")

        # Тестируем загрузку данных
        data_handler = MetalsData(file_path)
        if data_handler._data:
            print(f"✅ Данные загружены. Записей: {len(data_handler._data)}")

            # Показываем пример данных
            dates = list(data_handler._data.keys())
            if dates:
                first_date = dates[0]
                last_date = dates[-1]
                print(f"✅ Первая запись: {first_date} -> {data_handler._data[first_date]}")
                print(f"✅ Последняя запись: {last_date} -> {data_handler._data[last_date]}")
        else:
            print("❌ Данные не загружены")
    else:
        print("❌ Файл не создан")


if __name__ == "__main__":
    test_parser()