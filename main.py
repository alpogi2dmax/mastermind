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

    correct_position = 0
    correct_number = 0
    prev_guess = []

    for i in range(len(guess)):
        if guess[i] == secret[i]:
            correct_position += 1
        if guess[i] in secret and guess[i] not in prev_guess:
            correct_number += 1
            prev_guess.append(guess[i])

    return correct_position, correct_number

def main():
    secret = generate_code()
    # secret = [0, 1, 3, 5]
    print('Welcome to Matermind! Guess the 4-digit code(numbers 0-7).')
    attempts = 10
    history = []

    for attempt in range(1, attempts + 1):
        while True:
            user_input = input(f'\nAttempt {attempt}/{attempts}: Enter 4 numbers separated by spaces: ')
            try:
                guess = [int(x) for x in user_input.strip().split()]
                if len(guess) != 4 or any(x < 0 or x > 7 for x in guess):
                    raise ValueError
                break
            except ValueError:
                print('Invalid input. Enter exactly 4 numbers from 0 to 7 separated by spaces.')

        correct_pos, correct_num = evaluate_guess(secret, guess)
        history.append((guess, correct_pos, correct_num))

        if (correct_pos == 0 and correct_num == 0):
            print(f'Feedback: all incorrect')
        else:
            print(f"Feedback: {correct_num} correct number and {correct_pos} correct location")
        
        print('History:')
        for h in history:
            print(f'  Guess: {h[0]} -> {h[2]} correct number and {h[1]} correct location')

        if correct_pos == 4:
            print('\nCongratulations! You guessed the code!')
            break
    
    else:
        print('\n Game Over! You ran out of attempts.')
        print(f'The secret code was {secret}')

if __name__ == '__main__':
    main()

    # secret = generate_code()
    # print('Generated secret code:', secret)

    # guesses = [
    #     [0, 0, 0, 0],
    #     [secret[0], secret[1], 0, 0],
    #     secret
    # ]

    # for guess in guesses:
    #     pos, num = evaluate_guess(secret, guess)
    #     print(f'Guess: {guess} -> {pos} correct position, {num} correct number')