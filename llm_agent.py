class LLMAgent:
    def get_action(self, messages, tools):
        text = messages[-1]["content"].lower()

        if "schedule" in text:
            return "get_employee_id", {"name": "John"}

        if "employee" in text:
            return "check_calendar", {"employee_id": "EMP123"}

        if "calendar" in text:
            return "book_meeting", {"time": "10AM"}

        return None, None