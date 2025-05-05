# Чтение списка ИНН из traders.txt
with open('traders.txt', 'r', encoding='utf-8') as f:
    inn_list = [line.strip() for line in f if line.strip()]  # Удаляем пустые строки

# Проверка
print(f"Найдено ИНН: {len(inn_list)}")
print(f"Пример ИНН: {inn_list[:3]}")

import json

# Загрузка данных из traders.json
with open('traders.json', 'r', encoding='utf-8') as f:
    traders_data = json.load(f)  # Предполагается, что данные в формате списка словарей

# Фильтрация организаций по ИНН
filtered_traders = []
for trader in traders_data:
    if trader.get('inn') in inn_list:
        filtered_traders.append(trader)

# Проверка
print(f"Найдено организаций: {len(filtered_traders)}")

import csv

# Создание CSV-файла
with open('traders.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ИНН', 'ОГРН', 'Адрес'])  # Заголовки

    for trader in filtered_traders:
        # Извлекаем данные, заменяем отсутствующие значения на "Нет данных"
        inn = trader.get('inn', 'Нет данных')
        ogrn = trader.get('ogrn', 'Нет данных')
        address = trader.get('address', 'Нет данных')
        writer.writerow([inn, ogrn, address])

print("Файл traders.csv создан!")

import re

def find_emails(text):
    # Регулярное выражение для поиска email-адресов
    pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    emails = re.findall(pattern, text, flags=re.IGNORECASE)
    return emails


import re
import json


# Функция для поиска email-адресов
def find_emails(text):
    # Регулярное выражение для email (учитывает кириллические домены, например .рф)
    pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,}|\.xn--[a-zA-Z0-9]+)\b'
    emails = re.findall(pattern, text, flags=re.IGNORECASE)
    return emails


# Загрузка датасета
try:
    with open('1000_efrsb_messages.json', 'r', encoding='utf-8') as f:
        messages = json.load(f)  # Данные в формате списка словарей
except FileNotFoundError:
    print("Ошибка: Файл 1000_efrsb_messages.json не найден в рабочей директории!")
    exit()

# Сбор email-адресов по ИНН
email_dict = {}

for message in messages:
    # Извлекаем ИНН публикатора и текст сообщения
    inn = message.get('publisher_inn')
    text = message.get('msg_text', '')

    # Пропускаем записи без ИНН или текста
    if not inn or not text:
        continue

    # Ищем email-адреса
    emails = find_emails(text)

    # Добавляем в словарь
    if emails:
        if inn not in email_dict:
            email_dict[inn] = set()
        email_dict[inn].update(emails)

# Конвертируем множества в списки для JSON
formatted_data = {inn: list(emails) for inn, emails in email_dict.items()}

# Сохраняем результат
with open('emails.json', 'w', encoding='utf-8') as f:
    json.dump(formatted_data, f, ensure_ascii=False, indent=4)

print("Готово! Результаты сохранены в emails.json.")

