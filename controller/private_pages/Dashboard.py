from flask import request, session
from ...renderer import template_render
from ..protected_pages.plot_creator import Plot_Creator
from ..protected_pages.get_crypto_data import GetCryptoData
from ..protected_pages.user_data import User_data


USER_ID = session.get('user_id')
DIGITS = []


class Dashboard:
    def __init__(self):
        self.user_data = User_data() #cria uma instancia da classe responsavel pelos dados do usuário
        self.data = GetCryptoData() #cria uma instancia da classe responsavel pelos dados das moedas
        self.dashboard = Plot_Creator() #cria uma instancia da classe responsavel por gerar os graficos
        self.verificado = self.user_data.get_4_digits_pass(user_id=USER_ID)

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
        session['profile_img'] = self.user_data.get_profile_img(USER_ID)
        self.data.do_update_database() #atualiza o banco das criptomoedas

        #pega todas as informações do dashboard, coloca no dict(data) e renderiza o dashboard.html
        btc_plot = self.dashboard.create_plot_range_value('bitcoin')
        eth_plot = self.dashboard.create_plot_range_value('ethereum')
        btc_history_plot = self.dashboard.create_plot_history('bitcoin', USER_ID)
        eth_history_plot = self.dashboard.create_plot_history('ethereum', USER_ID)
        spent_plot_6 = self.dashboard.create_plot_spent(user_id=USER_ID, time='6')
        spent_plot_all = self.dashboard.create_plot_spent(user_id=USER_ID, time='all')

        data = {
            'btc_plot': btc_plot,
            'eth_plot': eth_plot,
            'btc_history_plot': btc_history_plot,
            'eth_history_plot': eth_history_plot,
            'spent_plot_6': spent_plot_6[0] if spent_plot_6 else None,
            'spent_plot_all': spent_plot_all[0] if spent_plot_all else None,
            'spent_1_month': f'{spent_plot_6[1][0][1]:.2f}' if spent_plot_6 else None,
            'title': "Bitcoin",
            'last_buy_date': self.data.get_last_buy_date(USER_ID),
            'last_trade_data': self.data.get_last_trade_data(USER_ID),
            'verificado': self.verificado #verifica se o usuario tem a senha de 4 digitos
        }

        #verifica se o usuario tem a senha de 4 digitos, se n tiver exibe o modal e vai pedir a 
        #senha de 4 digitos. Se o usuario tiver uma senha, ou a sua senha for aprovada, nao vai mais exibir

        if not self.verificado:
            if session["request_method"] == 'POST':
                if request.form.get('submit_4_digits_form'):
                    msg = self.verify_password()

                    if DIGITS == msg:
                        password = ''.join(DIGITS[0])  
                        self.user_data.set_4_digits_pass(password, user_id=USER_ID)
                        return template_render('dashboard.html', **data, stats=True)
  
        return template_render('dashboard.html', **data)