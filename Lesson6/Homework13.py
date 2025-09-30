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

        print(f"Все данные успешно сохранены в {self.json_filename}")

    def _add_data(self, date, rate):
        """Приватный метод для добавления данных в словарь"""
        self.data[date] = rate


class CBRFHTMLParser(HTMLParser):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.in_table = False
        self.in_row = False
        self.cell_count = 0
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
                    self.parent._add_data(date, rate)  # Используем приватный метод
                except ValueError:
                    pass
            self.cell_data = []

    def handle_data(self, data):
        if self.in_row and self.cell_count > 0 and data.strip():
            # Добавляем данные из ячейки
            if len(self.cell_data) < self.cell_count:
                self.cell_data.append(data.strip())


if __name__ == "__main__":
    # Создаем парсер
    parser = ParserCBRF()

    # Запускаем парсер и получаем все данные
    all_data = parser.start()

    # Выводим все данные в консоль
    print("\nВСЕ ДАННЫЕ ПО КЛЮЧЕВОЙ СТАВКЕ ЦБ РФ:")
    print("=" * 50)

    # Сортируем по дате и выводим все записи
    for date, rate in sorted(all_data.items()):
        print(f"{date}: {rate}%")

    # Выводим статистику
    print("\n" + "=" * 50)
    print(f"Всего записей: {len(all_data)}")

    if all_data:
        dates = sorted(all_data.keys())
        print(f"Период данных: с {dates[0]} по {dates[-1]}")
        print(f"Текущая ключевая ставка: {all_data[dates[-1]]}%")