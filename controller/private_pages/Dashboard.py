from flask import render_template, request, session
import os, sys, matplotlib

matplotlib.use('Agg')

# Adiciona o caminho do diretório pai para importações dos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..protected_pages.plot_creator import Plot_Creator
from ..protected_pages.get_crypto_data import GetCryptoData
from ..protected_pages.set_user_data import SetUserData

USER_ID = 1
DIGITS = []


#Classe responsavel por exibir o dashboard
class Dashboard:
    def __init__(self):
        self.data = GetCryptoData() #cria uma instancia da classe responsavel pelos dados do usuário/cripto
        self.dashboard = Plot_Creator() #cria uma instancia da classe responsavel por gerar os graficos
        self.verificado = True

    def get_default_data(self):
        #Pega os dados padrao q no caso é o do bitcoin
        self.dashboard.create_plot_range_value('bitcoin') #carrega o plot do btc atualizado
        self.dashboard.create_plot_history('bitcoin',  USER_ID)
        spent_plot = self.dashboard.create_plot_spent(user_id=USER_ID, time='1')
        return {
            'plot_url': '../static/images/dashboard/bitcoin.png',
            'history_plot_url': f'../static/images/dashboard/crypto_history_1_{USER_ID}.png',
            'title': "Bitcoin",
            'volume': self.data.get_volume('bitcoin'),
            'spent_plot_url': spent_plot[0],
            'spent_plot_data': spent_plot[1],
            'last_buy_date': self.data.get_last_buy_date(USER_ID),
            'last_trade_data': self.data.get_last_trade_data(USER_ID),
            'time': '1'
        }

    def get_crypto_data(self, crypto_name):
        #Pega os dados da moeda selecionada
        crypto_id = 1 if crypto_name == 'bitcoin' else 2
        self.dashboard.create_plot_range_value(crypto_name)
        self.dashboard.create_plot_history(crypto_id, USER_ID)
        return {
            'plot_url': os.path.join('../', 'static', 'images', 'dashboard', f'{crypto_name}.png'),
            'history_plot_url': os.path.join('../', 'static', 'images', 'dashboard', f'crypto_history_{crypto_id}_{USER_ID}.png'),
            'title': crypto_name.capitalize(),
            'volume': self.data.get_volume(crypto_name)
        }

    def update_spent_plot(self, total_spent):
        #Atualiza o grafico de gastos
        spent_plot = self.dashboard.create_plot_spent(user_id=USER_ID, time=total_spent)
        if spent_plot[0] == None:
            return {
                'spent_plot_url': None,
                'spent_plot_data': spent_plot[1],
                'time': total_spent
            }
        return{
            'spent_plot_url': f'images/dashboard/crypto_spent_{USER_ID}_{total_spent}.png',
            'spent_plot_data': spent_plot[1],
            'time': total_spent

        }
    
    def verify_password(self):
        #Verifica se a senha é de 4 digitos e se ela tem algum valor que nao seja numerico
        #Se um valor nao for numerico n é adicionado na tmp_digits, no final verifica se a tmp_digits tem os 4 digitos
        form_sent = request.form.get('submit_4_digits_form')
        tmp_digits = []
        for c in range(1, 5):
            digit = (request.form.get(f'digit-{c}'))
            if digit.isdigit():
                tmp_digits.append(digit)
        if form_sent:
            if len(tmp_digits) < 4:
                msg = 'Senha inválida, digite apenas valores numéricos de 0-9'
            else:
                DIGITS.append(tmp_digits)
                msg = DIGITS
            return msg

    def index(self):
        msg = ''
        stats = ''
        data = self.get_default_data()

        #verifica se o cara tem a senha de 4 digitos, se n tiver exibe o modal e vai pedir a senha de 4 digitos
        #verifica a senha e se for aprovada nao precisa mais fazer
        if not self.verificado:
            if session["request_method"] == 'POST':
                if request.form.get('submit_4_digits_form'):
                    msg = self.verify_password()
                    stats = 'denied'
                    if DIGITS == msg:
                        password = ''.join(DIGITS[0])  
                        SetUserData.define_4_digits_pass(password, USER_ID)
                        self.verificado = True
                        stats = 'aproved'

        if session["request_method"] == 'POST':            
            crypto_name = request.form.get('crypto') #verifica se foi pressionado   
            total_spent = request.form.get('total_spent', '1') 
            if crypto_name:
                data.update(self.get_crypto_data(crypto_name))  #altera o grafico entre btc-eth

            if total_spent:
                data.update(self.update_spent_plot(total_spent)) #altera o total spent entre 1 mes, 6 meses e ao todo

        return render_template('dashboard.html', **data, verificado=self.verificado, digits=DIGITS, msg=msg, stats=stats)


