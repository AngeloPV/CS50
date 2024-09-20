import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ...models.crypto_data import CryptoInfo
from ...models.update_criptocurrencies import CryptoUpdate

class SetUserData:
    def __init__(self):
        self.model = CryptoInfo()
        self.update = CryptoUpdate()

    @staticmethod
    def define_4_digits_pass(password, user_id):
        model = CryptoInfo()
        model.set_4_digits_pass(password, user_id)