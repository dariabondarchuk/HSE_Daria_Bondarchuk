import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


class ParserCBRF:
    def __init__(self, url=None):
        self.base_url = "https://www.cbr.ru"
        self.target_url = url or "https://www.cbr.ru/hd_base/keyrate/"
        self.data = {}

    def start(self):
        """Основной публичный метод для запуска парсера"""
        try:
            self._download_and_parse()
            return self.data
        except Exception as e:
            print(f"Ошибка при выполнении парсера: {e}")
            return {}

    def _download_and_parse(self):
        """Скачивание и парсинг данных с сайта ЦБ РФ"""
        # Загружаем страницу
        response = requests.get(self.target_url)
        response.raise_for_status()  # Проверяем успешность запроса

        # Парсим HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем таблицу с данными (класс 'data' часто используется на сайте ЦБ)
        table = soup.find('table', {'class': 'data'})

        if not table:
            print("Таблица с данными не найдена")
            return

        # Парсим строки таблицы
        for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
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
                    print(f"Ошибка преобразования данных: {date_str}, {rate_str} - {e}")
                    continue

    def save_to_file(self, filename="key_rates.txt"):
        """Дополнительный метод для сохранения данных в файл"""
        with open(filename, 'w', encoding='utf-8') as f:
            for date, rate in sorted(self.data.items()):
                f.write(f"{date}: {rate}\n")
        print(f"Данные сохранены в файл: {filename}")


# Пример использования
if __name__ == "__main__":
    # Создаем парсер
    parser = ParserCBRF()

    # Запускаем сбор данных
    result = parser.start()

    # Выводим результаты
    print(f"Найдено записей: {len(result)}")

    if result:
        print("\nПервые 10 записей:")
        for date, rate in sorted(result.items())[:10]:
            print(f"{date}: {rate}%")

        # Сохраняем в файл
        parser.save_to_file()

        # Выводим статистику
        dates = sorted(result.keys())
        print(f"\nДиапазон данных: с {dates[0]} по {dates[-1]}")
        print(f"Текущая ключевая ставка: {result[dates[-1]]}%")
    else:
        print("Данные не получены")