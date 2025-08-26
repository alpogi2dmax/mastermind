import time

GAME = {
    'secret': [],
    'history': [],
    'attempts': 0,
    'max_attempts': 10,
    'finished': False,
    'hint': [],
    'last_evaluation': {},
    'start_time': None,
    'end_time': None,
    'elapsed_time': None
}

def reset_game(secret_code):
    GAME['secret'] = secret_code
    GAME['history'] = []
    GAME['attempts'] = 0
    GAME['finished'] = False
    GAME['hint'] = ['__' for _ in secret_code]
    GAME['last_evaluation'] = {}
    GAME['start_time'] = time.time()
    GAME['end_time'] = None
    GAME['elapsed_time'] = None