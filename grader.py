def grade_easy(env):
    if env.done:
        return 0.9
    elif getattr(env, "employee_id", None):
        return 0.5
    else:
        return 0.2


def grade_medium(env):
    if env.done:
        return 0.85
    elif getattr(env, "calendar_checked", None):
        return 0.6
    else:
        return 0.3


def grade_hard(env):
    if env.done:
        return 0.8
    elif getattr(env, "calendar_checked", None):
        return 0.55
    else:
        return 0.25


def grade_veryhard(env):
    if env.done:
        return 0.75
    elif getattr(env, "calendar_checked", None):
        return 0.5
    else:
        return 0.2


def grade_extreme(env):
    if env.done:
        return 0.7
    elif getattr(env, "calendar_checked", None):
        return 0.45
    else:
        return 0.15


def grade_expert(env):
    if env.done:
        return 0.65
    elif getattr(env, "calendar_checked", None):
        return 0.4
    else:
        return 0.1


def grade_master(env):
    if env.done:
        return 0.6
    elif getattr(env, "calendar_checked", None):
        return 0.35
    else:
        return 0.05


def grade_legend(env):
    if env.done:
        return 0.95
    elif getattr(env, "calendar_checked", None):
        return 0.65
    else:
        return 0.3


def grade_godlike(env):
    if env.done:
        return 1.0
    elif getattr(env, "calendar_checked", None):
        return 0.7
    else:
        return 0.35


# Export all graders
__all__ = ['grade_easy', 'grade_medium', 'grade_hard', 'grade_veryhard', 'grade_extreme', 'grade_expert', 'grade_master', 'grade_legend', 'grade_godlike']
