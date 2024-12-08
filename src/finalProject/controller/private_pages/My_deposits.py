from ...renderer import template_render
from flask import session
from ...models.Deposit_data import Deposit_data
from ...models.User import User
USER_ID = session.get('user_id')

class My_deposits:
    """
    Classe responsavel por gerar o histórico de depósitos, o saldo do usuário e a situação de sua carteira
    """
    def __init__(self):
        self.data = Deposit_data() #intancia a classe responsavel pelos dados do deposito
        self.user = User() #intancia a classe responsavel pelos dados do usuario

    def index(self):
        """
        Renderiza a página com o histórico de depósitos do usuário, seu saldo e a situação de sua carteira
        """
        #pega o saldo do usuario
        session['balance'] = self.user.get_cash(user_id=session.get('user_id'))

        #pega todos os depositos e passa pra my_deposits.html
        data = {'deposits': self.data.get_deposit_history(user_id=USER_ID)}

        #pega os dados da carteira
        if self.user.get_wallet(user_id=session.get('user_id')):
            data['wallet'] = self.user.get_wallet(user_id=session.get('user_id'))
        return template_render('my_deposits.html', **data)
