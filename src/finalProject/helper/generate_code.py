import random
import string

def generate_random_code(length=6):
    """
    Gera um código de caracteres aleatórios com 6 digitos por padrão para ser usado na verificação por email.
    """
    characters = string.ascii_uppercase + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code

