import json
import csv
import re


def read_inn_from_file(file_path):
    """Считывает ИНН из файла traders.txt."""
    with open(file_path, 'r', encoding='utf-8') as file:
        inns = [line.strip() for line in file.readlines()]
    return inns


def get_organization_info(inns, json_file_path):
    """Получает информацию об организациях из файла traders.json по списку ИНН."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        organizations = json.load(file)

    result = []
    for inn in inns:
        org_info = next((org for org in organizations if org['inn'] == inn), None)
        if org_info:
            result.append({
                'inn': org_info['inn'],
                'ogrn': org_info['ogrn'],
                'address': org_info['address']
            })
    return result


def save_to_csv(data, csv_file_path):
    """Сохраняет информацию об ИНН, ОГРН и адресе в файл traders.csv."""
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['inn', 'ogrn', 'address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)


def find_emails(text):
    """Находит email-адреса в тексте и возвращает их список."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def extract_emails_from_dataset(dataset_file_path):
    """Извлекает email-адреса из датасета и собирает их в словарь."""
    emails_dict = {}

    with open(dataset_file_path, 'r', encoding='utf-8') as file:
        dataset = json.load(file)

        for entry in dataset:
            inn = entry['publisher_inn']
            msg_text = entry['msg_text']
            emails = find_emails(msg_text)

            if emails:
                if inn not in emails_dict:
                    emails_dict[inn] = set()
                emails_dict[inn].update(emails)

    return emails_dict


def save_emails_to_json(emails_dict, json_file_path):
    """Сохраняет собранные email-адреса в файл emails.json."""
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(emails_dict, jsonfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Путь к файлам
    traders_txt_path = 'traders.txt'
    traders_json_path = 'traders.json'
    traders_csv_path = 'traders.csv'
    dataset_path = 'dataset.json'  # Убедитесь, что у вас есть этот файл
    emails_json_path = 'emails.json'

    # Чтение ИНН из файла traders.txt
    inns = read_inn_from_file(traders_txt_path)

    # Получение информации об организациях
    organizations_info = get_organization_info(inns, traders_json_path)

    # Сохранение информации в traders.csv
    save_to_csv(organizations_info, traders_csv_path)

    # Извлечение email-адресов из датасета
    emails_dict = extract_emails_from_dataset(dataset_path)

    # Сохранение email-адресов в emails.json
    save_emails_to_json(emails_dict, emails_json_path)