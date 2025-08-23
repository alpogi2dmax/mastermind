import requests

def generate_code():

    url = 'https://www.random.org/integers/'

    params = {
        'num': 4,
        'min': 0,
        'max': 7,
        'col': 1,
        'base': 10,
        'format': 'plain',
        'rnd': 'new'
    }

    response = requests.get(url, params=params, headers={"User-Agent": "mastermind-game/1.0"}, timeout=5)

    if response.status_code != 200:
        raise RuntimeError(f'Random.org API error: {response.status_code}')
    
    numbers = response.text.strip().split('\n')
    return [int(num) for num in numbers]

def evaluate_guess(secret, guess):

    if len(secret) != len(guess):
        raise ValueError('Guess and secret must be the same length')
    
    # correct_position = sum(s == g for s, g in zip(secret, guess))

    # secret_counts = {}
    # guess_counts = {}

    # for s, g in zip(secret, guess):
    #     secret_counts[s] = secret_counts.get(s, 0) + 1
    #     guess_counts[g] = guess_counts.get(g, 0) + 1

    # total_correct = sum(min(secret_counts.get(num, 0), guess_counts.get(num, 0)) for num in guess_counts)

    # correct_number = total_correct - correct_position

    correct_position = 0
    correct_number = 0

    # Make copies to mark used numbers
    secret_copy = secret.copy()
    guess_copy = guess.copy()
    
    # First pass: exact matches
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            correct_position += 1
            secret_copy[i] = guess_copy[i] = None  # mark as used

    print(secret_copy)
    print(guess_copy)
    
    # Second pass: correct numbers in wrong positions
    for i in range(len(guess_copy)):
        if guess_copy[i] is not None and guess_copy[i] in secret_copy:
            correct_number += 1
            secret_copy[secret_copy.index(guess_copy[i])] = None  # mark as used

    return correct_position, correct_number

if __name__ == '__main__':
    secret = generate_code()
    print('Generated secret code:', secret)

    guesses = [
        [0, 0, 0, 0],
        [secret[0], secret[1], 0, 0],
        secret
    ]

    for guess in guesses:
        pos, num = evaluate_guess(secret, guess)
        print(f'Guess: {guess} -> {pos} correct position, {num} correct number')