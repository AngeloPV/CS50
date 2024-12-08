from flask import request, session, jsonify
from ...renderer import template_render
from ..protected_pages.plot_creator import Plot_Creator
from ..protected_pages.get_crypto_data import GetCryptoData
from ..protected_pages.user_data import User_data
from ..protected_pages.Count_notifications import Count_notifications
from ...models.User import User
from ...helper.valitade import Validate
from ...helper.postal_code import Postal_code
from ...app import processor_add_notifications_processor
import time

session.pop("user_email", None)
USER_ID = session.get('user_id')
DIGITS = []


class Dashboard:
    """
    Classe responsável por gerenciar as operações da página de dashboard do usuário.
    Contém funcionalidades para exibir gráficos, validar senhas e carregar informações do usuário.
    """
    def __init__(self):
        """
        Inicializa a classe Dashboard com dependências como dados do usuário,
        informações de criptomoedas e notificações.
        """
        self.user = User() #cria uma instancia responsavel por pegar as informações do usuário
        self.user_data = User_data() #cria uma instancia da classe responsavel pelos dados do usuário
        self.data = GetCryptoData() #cria uma instancia da classe responsavel pelos dados das moedas
        self.dashboard = Plot_Creator() #cria uma instancia da classe responsavel por gerar os graficos
        self.verificado = self.user_data.get_4_digits_pass(user_id=USER_ID)
        self.count_notifications = Count_notifications().get_count() #diz quantas noticações não lidas o usario possui
        self.validate = Validate() #cria uma instancia responsavel pela validação
        self.postal_code = Postal_code() #cria uma instancia responsavel por pegar a localização do usuário

        # a session view_count, irá ficar sendo usada para verificar se a pagina de notifcations ja foi acessado, caso tenha sido ent todas as notifacations pedentes ja foram vistas
        session['viewd_count'] = False

        # Verifica se a session contém a chave 'last_update_time', caso contrário define como 0
        if 'last_update_time' not in session:
            session['last_update_time'] = 0


    def verify_password(self):
        """
        Verifica a senha de 4 dígitos enviada pelo usuário, valida a senha e 
        retorna mensagem de erro ou armazena a senha válida.
        """
        form_sent = request.form.get('submit_4_digits_form')
        tmp_digits = []
        for c in range(1, 5):
            digit = (request.form.get(f'digit-{c}'))
            if digit.isdigit():
                tmp_digits.append(digit)
        if form_sent:
            if len(tmp_digits) < 4:
                msg = 'Invalid password, enter only numeric values from 0-9'
            else:
                DIGITS.append(tmp_digits)
                msg = DIGITS
            return msg
        
    def index(self):
        """
        Renderiza a página principal do dashboard com gráficos e informações personalizadas.
        Também gerencia o carregamento de temas e idiomas do usuário.
        """
        current_time = time.time()
        #Adicionando dados do usuário na sessão para que sejam usados no restante do site
        session['theme'] = self.user_data.get_theme(USER_ID)
        session['language'] = self.user_data.get_language(USER_ID)
        session['profile_img'] = self.user_data.get_profile_img(USER_ID)
        session['balance'] = self.user.get_cash(USER_ID)

        if not self.user.get_postal_code(USER_ID):
            cep = self.postal_code.get_coordinates_from_json()
            self.user.set_postal_code(USER_ID, cep)
        
        # Verifica se passaram mais de 30 segundos desde a última atualização
        # Essa verificação serve para saber se o usuario recarregou a pagina nos ultimos 30 segundos,
        # onde as informacoes so serao atualizadas de 30 em 30 segundos pois os plots pegam dados de
        # API, e para nao sobrecarregar as requisições é necessário um tempo entre cada atualizacao
        
        if current_time - session.get('last_update_time', 0) > 30:
            # Atualiza os dados e salva o timestamp da atualização
            session['last_update_time'] = current_time

            self.data.do_update_database() #atualiza o banco das criptomoedas

            #pega todas as informações do dashboard, coloca no dict(data) e renderiza o dashboard.html
            session['btc_plot'] = self.dashboard.create_plot_range_value('bitcoin')
            session['eth_plot'] = self.dashboard.create_plot_range_value('ethereum')
            session['btc_history_plot'] = self.dashboard.create_plot_history('bitcoin', USER_ID)
            session['eth_history_plot'] = self.dashboard.create_plot_history('ethereum', USER_ID)
            session['spent_plot_6'] = self.dashboard.create_plot_spent(user_id=USER_ID, time='6')
            session['spent_plot_all'] = self.dashboard.create_plot_spent(user_id=USER_ID, time='all')
            print(session['spent_plot_6'], 'session', '-'*55)

        data = {
            'btc_plot': session.get('btc_plot'),
            'eth_plot': session.get('eth_plot'),
            'btc_history_plot': session.get('btc_history_plot'),
            'eth_history_plot': session.get('eth_history_plot'),
            'spent_plot_6': session.get('spent_plot_6')[0] if session.get('spent_plot_6') else None,
            'spent_plot_all': session.get('spent_plot_all')[0] if session.get('spent_plot_all') else None,

            # Verifica se existe algo no índice onde era pra estar o total gasto no mês, caso não, 
            # retorna None
            'spent_1_month': f'${session.get("spent_plot_6")[1]:.2f}' if session.get('spent_plot_6') 
                            else None,

            'title': "Bitcoin",
            'last_buy_date': self.data.get_last_buy_date(USER_ID),
            'last_trade_data': self.data.get_last_trade_data(USER_ID),
            'verificado': self.verificado  # Verifica se o usuário tem a senha de 4 dígitos
        }

        #verifica se o usuario tem a senha de 4 digitos, se n tiver exibe o modal e vai pedir a 
        #senha de 4 digitos. Se o usuario tiver uma senha, ou a sua senha for aprovada, nao vai mais exibir

        if not self.verificado:
            if session["request_method"] == 'POST':
                if request.form.get('submit_4_digits_form'):
                    msg = self.verify_password()

                    if DIGITS == msg:
                        password_joined = ''.join(DIGITS[0])  
                        password = self.validate.encryption(user_password=password_joined)
                        self.user_data.set_4_digits_pass(password, user_id=USER_ID)
                        print(self.count_notifications)
                        return template_render('dashboard.html', **data, stats=True)
  
        return template_render('dashboard.html', **data)
    
    def clear_session():
        session.clear()
        return '', 200 