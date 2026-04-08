import random

class SecretaryEnv:
    def __init__(self, difficulty="hard"):
        self.difficulty = difficulty
        self.reset()

    def reset(self, **kwargs):
        """
        Reset environment

        Returns:
            Natural language instruction
        """
        self.valid_employees = {
            "John": "EMP123",
            "Alice": "EMP456"
        }

        self.employee_name = random.choice(list(self.valid_employees.keys()))
        self.employee_id = None
        self.calendar_checked = False
        self.available_slots = []
        self.meeting_booked = False

        self.reward = 0
        self.done = False
        self.steps = 0
        self.max_steps = 4

        return f"Schedule a meeting with {self.employee_name}"

    def _step_guard(self):
        self.steps += 1
        if self.steps > self.max_steps:
            self.reward = -1
            self.done = True
            raise ValueError("Step limit exceeded")

    def get_employee_id(self, name: str) -> str:
        """
        Get employee ID

        Args:
            name: employee name

        Returns:
            employee ID
        """
        self._step_guard()

        if name not in self.valid_employees:
            self.reward = -1
            raise ValueError("Employee not found")

        self.employee_id = self.valid_employees[name]
        self.reward = 0.3

        return f"Employee ID: {self.employee_id}"

    def check_calendar(self) -> str:
        """
        Check calendar availability

        Returns:
            available time slots
        """
        self._step_guard()

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

    def book_meeting(self, time: str) -> str:
        """
        Book meeting

        Args:
            time: selected slot

        Returns:
            confirmation message
        """
        self._step_guard()

        if not self.calendar_checked:
            self.reward = -1
            raise ValueError("Check calendar first")

        if time not in self.available_slots:
            self.reward = -0.5
            raise ValueError("Invalid time")

        if self.difficulty == "hard" and random.random() < 0.3:
            self.reward = -0.5
            raise ValueError("Booking failed")

        self.meeting_booked = True
        self.reward = 1.0
        self.done = True

        return f"Meeting booked at {time}"