import random


class SecretaryEnv:
    def __init__(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.1  # Start at 0.1 to stay strictly > 0.0
        self.done = False
        self.difficulty = "easy"

    def reset(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.1
        self.done = False
        
        if self.difficulty == "easy":
            return "Schedule a meeting with employee named John."
        elif self.difficulty == "medium":
            return "Find the ID for Alice and check her calendar to book a slot."
        else:
            return "Coordinate a meeting with Bob by checking his availability and booking a time."

    def _step_guard(self):
        pass

    def get_employee_id(self, name: str = "John"):
        # We accept any name to be flexible
        self.employee_id = f"EMP_{name.upper()}_123"
        self.reward += 0.1
        return f"Employee ID for {name} is {self.employee_id}"

    def check_calendar(self, employee_id: str = None):
        if employee_id:
            self.employee_id = employee_id

        if not self.employee_id:
            raise ValueError("Get employee ID first")

        self.available_slots = ["10AM", "2PM", "4PM"]
        self.calendar_checked = True
        self.reward += 0.2
        return f"Available slots: {', '.join(self.available_slots)}"

    def book_meeting(self, time: str = "10AM"):
        if not self.calendar_checked:
            raise ValueError("Check calendar first")

        self.done = True
        self.reward += 0.5 # Total reward: 0.1 (init) + 0.1 (id) + 0.2 (cal) + 0.5 (book) = 0.9
        return f"Meeting booked successfully at {time}"
