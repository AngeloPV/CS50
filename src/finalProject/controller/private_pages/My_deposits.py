from ...renderer import template_render
from flask import session
from ...models.Deposit_data import Deposit_data
from ...models.User import User
USER_ID = session.get('user_id')

class My_deposits:
    def __init__(self):
        self.data = Deposit_data()
        self.user = User()

    def index(self):
        session['balance'] = self.user.get_cash(user_id=session.get('user_id'))
        #pega todos os depositos e passa pra my_deposits.html
        data = self.data.get_deposit_history(user_id=USER_ID)
        return template_render('my_deposits.html', data=data)
