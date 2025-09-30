from urllib.request import urlopen
from html.parser import HTMLParser
from datetime import datetime
import ssl
import json
import os

# Отключаем проверку SSL для избежания ошибок с сертификатами
ssl._create_default_https_context = ssl._create_unverified_context


class ParserCBRF:
    def __init__(self, url=None, json_filename="cbrf_data.json"):
        self.base_url = "https://www.cbr.ru"
        self.target_url = url or "https://www.cbr.ru/hd_base/keyrate/"
        self.json_filename = json_filename
        self.data = {}
        self.current_date = None
        self.current_rate = None
        self.in_table = False
        self.in_row = False
        self.cell_count = 0

    def start(self):
        """Основной публичный метод для запуска парсера"""
        try:
            self._download_and_parse()
            self._save_to_json()
            return self.data
        except Exception as e:
            print(f"Ошибка при выполнении парсера: {e}")
            return {}

    def _download_and_parse(self):
        """Скачивание и парсинг данных с сайта ЦБ РФ"""
        # Загружаем страницу
        with urlopen(self.target_url) as response:
            html_content = response.read().decode('utf-8')

        # Парсим HTML
        parser = CBRFHTMLParser(self)
        parser.feed(html_content)

    def _save_to_json(self):
        """Приватный метод для сохранения данных в JSON"""
        # Преобразуем даты в строки для JSON-совместимости
        json_data = {str(date): rate for date, rate in self.data.items()}

        with open(self.json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        print(f"Данные успешно сохранены в {self.json_filename}")

    def add_data(self, date, rate):
        """Добавление данных в словарь"""
        self.data[date] = rate


class CBRFHTMLParser(HTMLParser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.in_table = False
        self.in_row = False
        self.cell_count = 0
        self.current_date = None
        self.current_rate = None
        self.cell_data = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            # Проверяем, что это таблица с данными
            for attr, value in attrs:
                if attr == 'class' and 'data' in value:
                    self.in_table = True
        elif self.in_table and tag == 'tr':
            self.in_row = True
            self.cell_count = 0
            self.cell_data = []
        elif self.in_row and tag == 'td':
            self.cell_count += 1

    def handle_endtag(self, tag):
        if tag == 'table' and self.in_table:
            self.in_table = False
        elif tag == 'tr' and self.in_row:
            self.in_row = False
            # Если у нас есть 2 ячейки с данными, обрабатываем их
            if len(self.cell_data) >= 2:
                date_str = self.cell_data[0]
                rate_str = self.cell_data[1]
                try:
                    date = datetime.strptime(date_str, '%d.%m.%Y').date()
                    rate = float(rate_str.replace(',', '.'))
                    self.parent.add_data(date, rate)
                except ValueError:
                    pass
            self.cell_data = []

    def handle_data(self, data):
        if self.in_row and self.cell_count > 0 and data.strip():
            # Добавляем данные из ячейки
            if len(self.cell_data) < self.cell_count:
                self.cell_data.append(data.strip())


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
        print("5. Пример данных из JSON:")
        items = list(json_data.items())[:5]  # Первые 5 записей
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