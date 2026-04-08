import random


class SecretaryEnv:
    def __init__(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0
        self.difficulty = "easy"

    def _step_guard(self):
        pass

    def check_calendar(self, employee_id: str = None) -> str:
        """
        Check calendar availability

        Returns:
            available time slots
        """
        self._step_guard()

        if employee_id:
            self.employee_id = employee_id

        if not self.employee_id:
            self.reward = -1
            raise ValueError("Get employee ID first")

        if self.difficulty != "easy" and random.random() < 0.2:
            self.reward = -0.3
            raise ValueError("Calendar API failed")

        self.available_slots = ["10AM", "2PM"]
        self.calendar_checked = True
        self.reward = 0.3

        return f"Available slots: {', '.join(self.available_slots)}"