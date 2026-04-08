import random


class SecretaryEnv:
    def __init__(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0
        self.done = False
        self.difficulty = "easy"

    def reset(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0
        self.done = False
        self.difficulty = "easy"

        return "Schedule a meeting with employee named John"

    def _step_guard(self):
        pass

    def get_employee_id(self, name: str = "John"):
        self.employee_id = "EMP123"
        self.reward += 0.2
        return f"Employee ID for {name} is {self.employee_id}"

    def check_calendar(self, employee_id: str = None) -> str:
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
        self.reward += 0.3

        return f"Available slots: {', '.join(self.available_slots)}"

    def book_meeting(self, time: str):
        if not self.calendar_checked:
            self.reward = -1
            raise ValueError("Check calendar first")

        if time not in self.available_slots:
            self.reward = -0.5
            raise ValueError("Invalid time slot")

        self.done = True
        self.reward += 1

        return f"Meeting booked at {time}"