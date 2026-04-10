def grade_easy(env):
    """
    Easy task grading
    """
    if env.meeting_booked:
        return 0.9   # ❗ NOT 1.0
    elif env.employee_id:
        return 0.5
    else:
        return 0.2


def grade_medium(env):
    """
    Medium task grading
    """
    if env.meeting_booked:
        return 0.85
    elif env.calendar_checked:
        return 0.6
    else:
        return 0.3


def grade_hard(env):
    """
    Hard task grading
    """
    if env.meeting_booked:
        return 0.8
    elif env.calendar_checked:
        return 0.55
    else:
        return 0.25
