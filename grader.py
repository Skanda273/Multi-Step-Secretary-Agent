def grade_easy(env):
    """
    Easy task grading
    """
    if env.done:
        return 0.9   # not 1.0
    elif env.employee_id:
        return 0.5
    else:
        return 0.2


def grade_medium(env):
    """
    Medium task grading
    """
    if env.done:
        return 0.85
    elif env.calendar_checked:
        return 0.6
    else:
        return 0.3


def grade_hard(env):
    """
    Hard task grading
    """
    if env.done:
        return 0.8
    elif env.calendar_checked:
        return 0.55
    else:
        return 0.25


def grade_veryhard(env):
    """
    Very hard task grading
    """
    if env.done:
        return 0.75
    elif env.calendar_checked:
        return 0.5
    else:
        return 0.2


def grade_extreme(env):
    """
    Extreme task grading
    """
    if env.done:
        return 0.7
    elif env.calendar_checked:
        return 0.45
    else:
        return 0.15


def grade_expert(env):
    """
    Expert task grading
    """
    if env.done:
        return 0.65
    elif env.calendar_checked:
        return 0.4
    else:
        return 0.1


def grade_master(env):
    """
    Master task grading
    """
    if env.done:
        return 0.6
    elif env.calendar_checked:
        return 0.35
    else:
        return 0.05


def grade_legend(env):
    """
    Legend task grading
    """
    if env.done:
        return 0.95
    elif env.calendar_checked:
        return 0.65
    else:
        return 0.3


def grade_godlike(env):
    """
    Godlike task grading
    """
    if env.done:
        return 1.0
    elif env.calendar_checked:
        return 0.7
    else:
        return 0.35


# Export all graders for validation and discovery
__all__ = ['grade_easy', 'grade_medium', 'grade_hard', 'grade_veryhard', 'grade_extreme', 'grade_expert', 'grade_master', 'grade_legend', 'grade_godlike']
