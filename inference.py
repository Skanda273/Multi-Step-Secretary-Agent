from env import SecretaryEnv


def run_episode(task=None):
    env = SecretaryEnv()
    instruction = env.reset()

    logs = []

    # step 1
    result = env.get_employee_id("John")
    logs.append({"action": "get_employee_id", "result": result})

    # step 2
    result = env.check_calendar(env.employee_id)
    logs.append({"action": "check_calendar", "result": result})

    # step 3
    result = env.book_meeting("10AM")
    logs.append({"action": "book_meeting", "result": result})

    return {
        "reward": env.reward,
        "steps": logs
    }


def main():
    output = run_episode()
    print(output)


if __name__ == "__main__":
    main()