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

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise RuntimeError(f'Random.org API error: {response.status_code}')
    
    numbers = response.text.strip().split('\n')
    return [int(num) for num in numbers]

if __name__ == '__main__':
    secret = generate_code()
    print('Generated secret code:', secret)