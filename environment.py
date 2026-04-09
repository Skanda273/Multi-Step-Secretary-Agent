import random


class SecretaryEnv:
    def __init__(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.01  # Start with a tiny non-zero value to stay > 0.0
        self.done = False
        self.difficulty = "easy"

    def reset(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.01
        self.done = False
        self.difficulty = "easy"

        return "Schedule a meeting with employee named John"

    def _step_guard(self):
        pass

    def get_employee_id(self, name: str = "John"):
        self.employee_id = "EMP123"
        self.reward += 0.1
        return f"Employee ID for {name} is {self.employee_id}"

    def check_calendar(self, employee_id: str = None):
        if employee_id:
            self.employee_id = employee_id

        if not self.employee_id:
            raise ValueError("Get employee ID first")

        self.available_slots = ["10AM", "2PM"]
        self.calendar_checked = True
        self.reward += 0.2
        return f"Available slots: {', '.join(self.available_slots)}"

    def book_meeting(self, time: str = None):
        if not self.calendar_checked:
            raise ValueError("Check calendar first")

        if time is None:
            time = self.available_slots[0]

        self.done = True
        self.reward += 0.6 # Total reward will be 0.01 + 0.1 + 0.2 + 0.6 = 0.91

        return f"Meeting booked at {time}"
