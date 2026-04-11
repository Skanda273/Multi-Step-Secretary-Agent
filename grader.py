def grade_easy(env):
    if env.done:                # ✅ correct attribute
        return 0.9
    elif env.employee_id:
        return 0.5
    else:
        return 0.2

def grade_medium(env):
    if env.done:
        return 0.85
    elif env.calendar_checked:
        return 0.6
    else:
        return 0.3

def grade_hard(env):
    if env.done:
        return 0.8
    elif env.calendar_checked:
        return 0.55
    else:
        return 0.25