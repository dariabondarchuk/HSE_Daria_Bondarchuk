class CourtCase:
    def __init__(self, case_number: str):
        self.case_number = case_number                  # обязательный параметр
        self.case_participants = []                     # список участников
        self.listening_datetimes = []                   # список заседаний
        self.is_finished = False                        # по умолчанию False
        self.verdict = ""                               # решение (по умолчанию пустое)

    def set_a_listening_datetime(self, datetime_info):
        """Добавить дату и время заседания"""
        self.listening_datetimes.append(datetime_info)

    def add_participant(self, participant):
        """Добавить участника (например, ИНН)"""
        if participant not in self.case_participants:
            self.case_participants.append(participant)

    def remove_participant(self, participant):
        """Удалить участника из списка"""
        if participant in self.case_participants:
            self.case_participants.remove(participant)

    def make_a_decision(self, verdict: str):
        """Вынести решение по делу"""
        self.verdict = verdict
        self.is_finished = True