import signal

def get_action_timed(agent, state, time_limit):
    action = None
    def signal_handler(signum, frame):
        raise Exception("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.setitimer(signal.ITIMER_REAL, time_limit)
    try:
        action = agent.get_action(state)
    except Exception as e:
        pass
    signal.setitimer(signal.ITIMER_REAL, 0)
    return action