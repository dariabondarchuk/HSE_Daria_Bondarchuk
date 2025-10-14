# -*- coding: utf-8 -*-

import json
import requests
import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup

# --- ШАГ 1: Определяем источник данных ---
DATA_URL = "https://cbr.ru/hd_base/metall/metall_base_new/"


# --- ШАГ 6: Оборачиваем парсер в класс ---
class PreciousMetalsParser:
    """
    Класс для сбора, обработки и сохранения учетных цен на драгоценные металлы.
    """

    def __init__(self, url: str):
        self.url = url
        self.save_path = Path('parsed_data') / 'precious_metals.json'
        self.metal_codes = {
            1: "Золото",
            2: "Серебро",
            3: "Платина",
            4: "Палладий"
        }

    def _get_html(self) -> str:
        """Скачивает HTML-код страницы."""
        print(f"Загружаю страницу: {self.url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            exit()

    def _parse_data(self, html: str) -> dict:
        """
        Извлекает данные из HTML и складывает их в словарь.
        Структура: {datetime.date: {metal_name: Decimal(price), ...}}
        """
        print("Начинаю парсинг данных...")
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('table', class_='data')

        if not table:
            print("Ошибка: не удалось найти таблицу с данными на странице.")
            exit()

        data = {}

        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if not cells:
                continue

            try:
                date_str = cells[0].text.strip()
                current_date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()

                prices = {}
                for i, code in self.metal_codes.items():
                    # <--- ИЗМЕНЕНИЕ: Добавляем .replace(' ', '') для удаления пробелов --->
                    price_str = cells[i].text.strip().replace(',', '.').replace(' ', '')
                    prices[code] = Decimal(price_str)

                data[current_date] = prices

            except (ValueError, IndexError, InvalidOperation) as e:
                # Теперь эта ошибка не должна появляться, но оставим на всякий случай
                print(f"Предупреждение: не удалось обработать строку. Ошибка: {e}")
                continue

        print(f"Парсинг завершен. Собрано {len(data)} записей.")
        return data

    def _fill_gaps(self, data: dict) -> dict:
        """
        Заполняет пропуски в данных (выходные и праздничные дни).
        """
        if not data:
            return {}

        print("Заполняю пропуски в данных (выходные дни)...")

        sorted_dates = sorted(data.keys())
        start_date, end_date = sorted_dates[0], sorted_dates[-1]

        filled_data = {}
        current_day = start_date
        last_known_prices = data[start_date]

        while current_day <= end_date:
            if current_day in data:
                last_known_prices = data[current_day]

            filled_data[current_day] = last_known_prices
            current_day += datetime.timedelta(days=1)

        print("Заполнение пропусков завершено.")
        return filled_data

    def _save_to_json(self, data: dict):
        """Сохраняет данные в JSON-файл."""
        print(f"Сохраняю данные в файл: {self.save_path}")
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        serializable_data = {
            date.isoformat(): {metal: str(price) for metal, price in prices.items()}
            for date, prices in data.items()
        }

        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=4)
        print("Данные успешно сохранены.")

    def start(self):
        """Главный метод, запускающий все шаги парсинга."""
        html = self._get_html()
        raw_data = self._parse_data(html)
        if not raw_data:
            print("Не удалось собрать данные. Сохранение и дальнейшая обработка отменены.")
            return

        filled_data = self._fill_gaps(raw_data)
        self._save_to_json(filled_data)


# --- ШАГ 7: Создаем класс для работы с собранными данными ---
class MetalsData:
    """
    Класс-"архивариус" для удобной работы с сохраненными данными о ценах на металлы.
    """

    def __init__(self, data_path: Path):
        self._data = self._load_data(data_path)
        self._sorted_dates = []
        if self._data:
            self._sorted_dates = sorted(self._data.keys())

    def _load_data(self, data_path: Path) -> dict:
        """Загружает и десериализует данные из JSON-файла."""
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Данные из {data_path} успешно загружены.")
            return data
        except FileNotFoundError:
            print(f"Информационное сообщение: файл {data_path} еще не создан.")
            return {}
        except json.JSONDecodeError:
            print(f"Ошибка! Не удалось прочитать JSON-файл {data_path}.")
            return {}

    def get_prices_on_date(self, date: str) -> dict | None:
        """
        Возвращает словарь с ценами на все металлы на определённую дату.
        """
        return self._data.get(date)

    def get_last_prices(self) -> dict | None:
        """
        Возвращает словарь с ценами на последнюю доступную дату.
        """
        if not self._data:
            return None
        last_date = self._sorted_dates[-1]
        return {"date": last_date, "prices": self._data[last_date]}

    def get_metal_price_for_period(self, metal_name: str, from_date: str, to_date: str) -> list[tuple]:
        """
        Возвращает отсортированный список пар (дата, цена) для одного металла
        за определённый период.
        """
        if metal_name not in ["Золото", "Серебро", "Платина", "Палладий"]:
            print(f"Ошибка: неверное название металла '{metal_name}'.")
            return []

        result = []
        for date_str in self._sorted_dates:
            if from_date <= date_str <= to_date:
                price = self._data[date_str].get(metal_name)
                if price:
                    result.append((date_str, price))
        return result


# --- Точка входа в программу ---
if __name__ == "__main__":

    # --- ЭТАП 1: Сбор и сохранение данных ---
    print("--- ЗАПУСК ПАРСЕРА ЦЕН НА МЕТАЛЛЫ ---")
    parser = PreciousMetalsParser(url=DATA_URL)
    parser.start()
    print("-" * 35)

    # --- ЭТАП 2: Работа с сохраненными данными ---
    print("\n--- ДЕМОНСТРАЦИЯ РАБОТЫ С ДАННЫМИ ---")

    data_handler = MetalsData(data_path=Path('parsed_data') / 'precious_metals.json')

    if data_handler._sorted_dates:
        last_date_str = data_handler._sorted_dates[-1]
        last_date = datetime.date.fromisoformat(last_date_str)
        # Устанавливаем начало периода на 6 дней раньше последней даты
        start_period = last_date - datetime.timedelta(days=6)

        # Пример 1: Получить цены на последнюю доступную дату
        print(f"\n1. Цены на металлы на последнюю дату ({last_date_str}):")
        prices = data_handler.get_prices_on_date(last_date_str)
        pprint(prices)

        # Пример 2: Получить историю цены на Золото за последние 7 дней
        print(f"\n2. Динамика цены на 'Золото' за последние 7 дней:")
        gold_prices = data_handler.get_metal_price_for_period(
            metal_name="Золото",
            from_date=start_period.isoformat(),
            to_date=last_date_str
        )
        for date, price in gold_prices:
            print(f"  {date}: {price} руб.")
    else:
        print("\nДанные для демонстрации отсутствуют.")