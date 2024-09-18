from ..renderer import template_render

from ..models.crypto_data import CryptoInfo

USER_ID = 1

class My_deposits:
    def __init__(self):
        self.data = CryptoInfo()

    def index(self):
        #pega todos os depositos e passa pra my_deposits.html
        data = self.data.get_deposit_history(user_id=USER_ID)
        return template_render('my_deposits.html', data=data)
