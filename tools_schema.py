tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_id",
            "description": "Look up and retrieve the employee ID for a given employee name. Always call this first before checking their calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Full name of the employee"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check the employee's calendar availability using their employee ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string", "description": "The employee's ID obtained from get_employee_id"}
                },
                "required": ["employee_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_meeting",
            "description": "Book a meeting at the specified time slot. Must be called after check_calendar to confirm availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "The time slot to book the meeting, e.g. '10AM' or '2PM'"}
                },
                "required": ["time"]
            }
        }
    }
]