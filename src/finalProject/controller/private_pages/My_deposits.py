from ...renderer import template_render
from flask import session
from ...models.Deposit_data import Deposit_data

USER_ID = session.get('user_id')

class My_deposits:
    def __init__(self):
        self.data = Deposit_data()

    def index(self):
        #pega todos os depositos e passa pra my_deposits.html
        data = self.data.get_deposit_history(user_id=USER_ID)
        return template_render('my_deposits.html', data=data)
