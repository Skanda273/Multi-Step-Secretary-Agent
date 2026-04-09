import random


class SecretaryEnv:
    def __init__(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.15  # Locked safe start score
        self.done = False
        self.difficulty = "easy"

    def reset(self):
        self.employee_id = None
        self.available_slots = []
        self.calendar_checked = False
        self.reward = 0.15
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
        self.employee_id = f"EMP_{name.upper()}_123"
        # Score remains 0.15 until final success to keep it simple
        return f"Employee ID for {name} is {self.employee_id}"

    def check_calendar(self, employee_id: str = None):
        if employee_id:
            self.employee_id = employee_id
        if not self.employee_id:
            raise ValueError("Get employee ID first")

        self.available_slots = ["10AM", "2PM", "4PM"]
        self.calendar_checked = True
        return f"Available slots: {', '.join(self.available_slots)}"

    def book_meeting(self, time: str = "10AM"):
        if not self.calendar_checked:
            raise ValueError("Check calendar first")

        self.done = True
        self.reward = 0.85 # Locked safe success score
        return f"Meeting booked successfully at {time}"
