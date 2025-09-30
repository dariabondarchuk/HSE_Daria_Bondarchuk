import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os


class ParserCBRF:
    def __init__(self, url=None, json_filename="key_rates.json"):
        self.base_url = "https://www.cbr.ru"
        self.target_url = url or "https://www.cbr.ru/hd_base/keyrate?UniDbQuery.Posted=True&UniDbQuery.From=01.01.2025&UniDbQuery.To=30.09.2025"
        self.json_filename = json_filename
        self.data = {}  # Структура для хранения: {дата: ставка}

    def start(self):
        """Единственный публичный метод для запуска парсера"""
        try:
            self._download_and_parse()
            self._save_to_json()
            self._display_all_data()
            return self.data
        except Exception as e:
            print(f"Ошибка при выполнении парсера: {e}")
            return {}

    def _download_and_parse(self):
        """Приватный метод: скачивание и парсинг данных с использованием BeautifulSoup"""
        print("Загрузка данных с сайта ЦБ РФ...")

        # Загружаем страницу
        response = requests.get(self.target_url)
        response.raise_for_status()

        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем таблицу с данными о ключевой ставке
        table = soup.find('table', {'class': 'data'})

        if not table:
            print("Таблица с данными не найдена!")
            return

        # Парсим все строки таблицы (кроме заголовка)
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)
                rate_str = cols[1].get_text(strip=True)

                try:
                    # Преобразуем дату и ставку
                    date = datetime.strptime(date_str, '%d.%m.%Y').date()
                    rate = float(rate_str.replace(',', '.'))
                    self.data[date] = rate
                except ValueError as e:
                    # Пропускаем некорректные данные
                    continue

        print(f"Загружено {len(self.data)} записей о ключевой ставке")

    def _save_to_json(self):
        """Приватный метод: сохранение данных в JSON"""
        # Преобразуем даты в строки для JSON-совместимости
        json_data = {str(date): rate for date, rate in self.data.items()}

        # Сортируем данные по дате (от старых к новым)
        sorted_data = {}
        for date in sorted(json_data.keys()):
            sorted_data[date] = json_data[date]

        with open(self.json_filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=2)

        print(f"Данные успешно сохранены в {self.json_filename}")

    def _display_all_data(self):
        """Приватный метод: отображение всех собранных данных"""
        if not self.data:
            print("Нет данных для отображения")
            return

        print(f"\n=== ВСЕ ДАННЫЕ ПО КЛЮЧЕВОЙ СТАВКЕ ЦБ РФ ===")
        print(f"Всего записей: {len(self.data)}")
        print("-" * 50)

        # Сортируем данные по дате
        sorted_items = sorted(self.data.items())

        # Выводим все данные
        for date, rate in sorted_items:
            print(f"{date}: {rate}%")

        print("-" * 50)

        # Статистика
        if sorted_items:
            print(f"Первая запись: {sorted_items[0][0]} - {sorted_items[0][1]}%")
            print(f"Последняя запись: {sorted_items[-1][0]} - {sorted_items[-1][1]}%")
            print(f"Текущая ключевая ставка: {sorted_items[-1][1]}%")

            # Анализ изменений ставки
            changes = []
            for i in range(1, len(sorted_items)):
                prev_rate = sorted_items[i - 1][1]
                curr_rate = sorted_items[i][1]
                if prev_rate != curr_rate:
                    changes.append((sorted_items[i][0], curr_rate, curr_rate - prev_rate))

            print(f"Количество изменений ставки: {len(changes)}")


# Функция для проверки выполнения задания
def check_parser_work():
    """Проверка корректности работы парсера"""
    print("=== ПРОВЕРКА ВЫПОЛНЕНИЯ ЗАДАНИЯ ===")

    # Создаем парсер
    parser = ParserCBRF(json_filename="key_rates.json")

    # Запускаем сбор данных
    print("1. Запуск парсера через parser.start()...")
    result = parser.start()

    # Проверяем, что данные получены
    print(f"2. Получено записей: {len(result)}")

    # Проверяем существование JSON-файла
    json_exists = os.path.exists("key_rates.json")
    print(f"3. JSON-файл создан: {json_exists}")

    if json_exists:
        # Проверяем содержимое JSON-файла
        with open("key_rates.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        print(f"4. Данные в JSON-файле: {len(json_data)} записей")

        # Выводим пример данных из JSON
        print("5. Пример данных из JSON (первые 10 записей):")
        items = list(json_data.items())[:10]
        for date, rate in items:
            print(f"   {date}: {rate}%")

        print("\nПример данных из JSON (последние 10 записей):")
        items = list(json_data.items())[-10:]
        for date, rate in items:
            print(f"   {date}: {rate}%")

    # Итоговая проверка
    success = len(result) > 0 and json_exists
    print(f"\n=== РЕЗУЛЬТАТ ПРОВЕРКИ: {'ЗАДАНИЕ ВЫПОЛНЕНО' if success else 'ЗАДАНИЕ НЕ ВЫПОЛНЕНО'} ===")

    return success


# Пример использования
if __name__ == "__main__":
    # Запускаем проверку
    check_parser_work()