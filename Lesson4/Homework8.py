class Contract:
    def __init__(self, contract_number, contract_type, signing_date):
        self.contract_number = contract_number  # Номер договора
        self.contract_type = contract_type  # Тип договора (поставки, аренды, услуг и т.д.)
        self.signing_date = signing_date  # Дата подписания
        self.parties = []  # Стороны договора
        self.terms = []  # Условия договора
        self.obligations = []  # Обязательства сторон
        self.rights = []  # Права сторон
        self.validity_period = None  # Срок действия договора
        self.termination_date = None  # Дата расторжения
        self.is_active = True  # Действует ли договор
        self.annexes = []  # Приложения к договору
        self.payment_terms = {}  # Условия платежей

    def add_party(self, party_name, party_role):
        """Добавление стороны договора"""
        self.parties.append({
            'name': party_name,
            'role': party_role  # Например: "заказчик", "исполнитель", "арендодатель"
        })

    def add_term(self, term_description):
        """Добавление условия договора"""
        self.terms.append(term_description)

    def add_obligation(self, obligation_description, responsible_party):
        """Добавление обязательства с указанием ответственной стороны"""
        self.obligations.append({
            'description': obligation_description,
            'responsible': responsible_party
        })

    def add_right(self, right_description, beneficiary_party):
        """Добавление права с указанием стороны-бенефициара"""
        self.rights.append({
            'description': right_description,
            'beneficiary': beneficiary_party
        })

    def set_validity_period(self, start_date, end_date):
        """Установление срока действия договора"""
        self.validity_period = {
            'start': start_date,
            'end': end_date
        }

    def add_annex(self, annex_title, annex_content):
        """Добавление приложения к договору"""
        self.annexes.append({
            'title': annex_title,
            'content': annex_content
        })

    def set_payment_terms(self, amount, currency, payment_schedule):
        """Установление условий платежей"""
        self.payment_terms = {
            'amount': amount,
            'currency': currency,
            'schedule': payment_schedule
        }

    def terminate_contract(self, termination_date, termination_reason):
        """Расторжение договора"""
        self.is_active = False
        self.termination_date = termination_date
        print(f"Договор №{self.contract_number} расторгнут {termination_date} по причине: {termination_reason}")

    def amend_contract(self, amendment_text, amendment_date):
        """Внесение изменений в договор"""
        self.terms.append(f"Поправка от {amendment_date}: {amendment_text}")

    def get_obligations_by_party(self, party_name):
        """Получение обязательств конкретной стороны"""
        party_obligations = []
        for obligation in self.obligations:
            if obligation['responsible'] == party_name:
                party_obligations.append(obligation['description'])
        return party_obligations

    def get_contract_summary(self):
        """Получение сводной информации о договоре"""
        summary = f"Договор №{self.contract_number} ({self.contract_type})\n"
        summary += f"Дата подписания: {self.signing_date}\n"
        summary += f"Статус: {'Действует' if self.is_active else 'Расторгнут'}\n"
        summary += f"Стороны: {', '.join([p['name'] + ' (' + p['role'] + ')' for p in self.parties])}\n"
        summary += f"Условий: {len(self.terms)}\n"
        summary += f"Обязательств: {len(self.obligations)}\n"
        summary += f"Прав: {len(self.rights)}\n"
        summary += f"Приложений: {len(self.annexes)}"

        if self.validity_period:
            summary += f"\nСрок действия: с {self.validity_period['start']} по {self.validity_period['end']}"

        if self.termination_date:
            summary += f"\nДата расторжения: {self.termination_date}"

        return summary


# Пример использования
if __name__ == "__main__":
    # Создаем договор
    contract = Contract(
        "Д-123/2023",
        "договор поставки",
        "2023-09-15"
    )

    # Добавляем стороны
    contract.add_party("ООО 'Поставщик Плюс'", "поставщик")
    contract.add_party("ИП Иванов И.И.", "покупатель")

    # Добавляем условия
    contract.add_term("Поставка осуществляется партиями по заявке покупателя.")
    contract.add_term("Качество товара должно соответствовать ГОСТ 12345-2020.")

    # Добавляем обязательства
    contract.add_obligation("Поставка товара в срок до 30 дней с момента получения заявки", "ООО 'Поставщик Плюс'")
    contract.add_obligation("Оплата товара в течение 10 банковских дней с момента получения", "ИП Иванов И.И.")

    # Добавляем права
    contract.add_right("Право на получение товара надлежащего качества", "ИП Иванов И.И.")
    contract.add_right("Право на получение оплаты в установленные сроки", "ООО 'Поставщик Плюс'")

    # Устанавливаем срок действия
    contract.set_validity_period("2023-09-15", "2024-09-14")

    # Добавляем приложения
    contract.add_annex("Спецификация товаров", "Перечень товаров с артикулами и ценами")
    contract.add_annex("График платежей", "План-график осуществления платежей по договору")

    # Устанавливаем условия платежей
    contract.set_payment_terms(500000, "RUB", "50% предоплата, 50% после поставки")

    # Используем методы договора
    print(contract.get_contract_summary())

    print("\nОбязательства поставщика:")
    for obligation in contract.get_obligations_by_party("ООО 'Поставщик Плюс'"):
        print(f"- {obligation}")

    # Вносим изменение в договор
    contract.amend_contract("Срок поставки изменен на 45 дней", "2023-10-01")

    # Расторгаем договор
    contract.terminate_contract("2023-11-20", "нарушение условий поставки")
    print(f"\nСтатус договора после расторжения: {contract.is_active}")