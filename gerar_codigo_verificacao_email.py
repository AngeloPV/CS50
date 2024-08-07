import random
import string

def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code

random_code = generate_random_code()
print(random_code)
