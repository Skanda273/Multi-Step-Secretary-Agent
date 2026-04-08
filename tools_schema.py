tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_id",
            "description": "Get employee ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check calendar",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_meeting",
            "description": "Book meeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {"type": "string"}
                },
                "required": ["time"]
            }
        }
    }
]