GAME = {
    'secret': [],
    'history': [],
    'attempts': 0,
    'max_attempts': 10,
    'finished': False,
    'hint': [],
    'last_evaluation': {}
}

def reset_game(secret_code):
    GAME['secret'] = secret_code
    GAME['history'] = []
    GAME['attempts'] = 0
    GAME['finished'] = False
    GAME['hint'] = ['__' for _ in secret_code]
    GAME['last_evaluation'] = {}