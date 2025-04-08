from flask import request, session, redirect, url_for
from ...renderer import template_render
from ...models.User import User
from ..protected_pages.get_crypto_data import GetCryptoData
from datetime import datetime

class Manage:
    """
    Esta classe gerencia o histórico de transações e os dados financeiros do usuário, como saldos 
    de criptomoedas e histórico de operações realizadas.
    """
    def __init__(self):
        self.data = GetCryptoData() # cria uma instancia da classe responsavel pelos dados das moedas
        self.user = User() # cria uma instancia da classe responsavel pelos dados do usuário


    def get_history_data(self, user_id):
        """
        Processa dados de compras, vendas e trocas realizadas pelo usuário e os organiza em uma única lista, 
        adicionando informações de tipo e data. A lista final é ordenada por data (mais recente primeiro).
        """
        # Pega os dados de todas as tabelas
        buy_data = self.user.get_buy_data(user_id)
        sell_data = self.user.get_sell_data(user_id)
        trade_data = self.user.get_trade_data(user_id)

        # Adcina um campo em comum a todos, no caso date e type
        for item in buy_data:
            item['type'] = 'buy'
            item['date'] = item['created']  

        for item in sell_data:
            item['type'] = 'sell'
            item['date'] = item['created']  

        for item in trade_data:
            item['type'] = 'trade'
            item['date'] = item['modified'] or item['created']  

        # Junta todas
        history_data = buy_data + sell_data + trade_data

        # Função auxiliar para converter strings de data em objetos datetime
        def parse_date(date_str):
            if isinstance(date_str, str) and date_str.replace('.', '', 1).isdigit():  # verifica se é um número
                # Se for um número não data, trata-o de outra forma ou retorna uma data padrão
                return datetime.min  # Ou outro valor padrão
            try:
                # se a data for uma string válida no formato esperado, converte para datetime
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # caso haja erro, retorna uma data padrão
                return datetime.min  # no caso seria a data mais antiga possível

        # Ordena os dados pelo campo de data, do mais recente ao mais antigo
        history_data.sort(
            key=lambda x: parse_date(str(x['date'])),
            reverse=True
        )

        # Retorna a history data
        return history_data


    def index(self):
        """
        Renderiza a página de gerenciamento, onde o usuário pode ver seu histórico de transações, ordenar
        por ações (compra, venda ou troca) e realizar a venda de suas criptomoedas.
        """
        #Limpa a sessão com os dados que foram usados para dar retorno ao usuario 
        if 'msg' in session:
            del session['msg']
        if 'currency' in session:
            del session['currency']
        if 'authorize' in session:
            del session['authorize']
        if 'not_authorize' in session:
            del session['not_authorize']
        # Verifica se ja existea currency_balance na sessão (a currency balance armazena os saldos das 
        # criptomoedas do usuario), se nao tiver na sessão, é armazenada o saldo de bitcoin na 
        # currency_balance['bitcoin], o mesmo vale pro ethereum. Após definir esses valores, não será mais feita
        # nenhuma requisição a API (codigo que faz a requisição = self.data.get_crypto_data_for_buy(['bitcoin', 'ethereum']))
        # as requisições serao feitas apenas quando o saldo das criptomoedas mudarem, isto é necessário para
        # não sobrecarregar o limite de requisições da API usada pra pegar os preços das criptomoedas

        if ('currency_balance' not in session or
            session['currency_balance'].get('bitcoin') != self.user.get_bitcoin_balance(session.get('user_id')) or
            session['currency_balance'].get('ethereum') != self.user.get_ethereum_balance(session.get('user_id'))):
            
            session['currency_balance'] = {'bitcoin': self.user.get_bitcoin_balance(session.get('user_id')),
                                           'ethereum': self.user.get_ethereum_balance(session.get('user_id'))}

            session['currency_data'] = self.data.get_crypto_data_for_buy(['bitcoin', 'ethereum'])

        #Dados a serem renderizados
        currency_data = session.get('currency_data')
        history_data = self.get_history_data(session.get('user_id'))
        print(self.get_history_data(session.get('user_id')), '-'*50)
        data = {
            'bitcoin_balance': session['currency_balance']['bitcoin'],
            'bitcoin_to_dol': currency_data.get('bitcoin', {}).get('current_price') * session['currency_balance']['bitcoin'],
            'ethereum_balance': session['currency_balance']['ethereum'],
            'ethereum_to_dol': currency_data.get('ethereum', {}).get('current_price') * session['currency_balance']['ethereum'],
            'history_data': history_data
        }

        #Retoma esses valores da sessão e passa para o template para serem usados pelo javascript
        msg = request.args.get('msg') #exibe a msg de erro
        currency = request.args.get('currency') #exibe a moeda a ser vendida
        authorize = request.args.get('authorize') #exibe um sweet alert de confirmacao
        not_authorize = request.args.get('not_authorize') #exibe um sweet alert de erro
        if msg:
            data['msg'] = msg
        if currency:
            data['currency'] = currency
        if authorize:
            data['authorize'] = authorize
        if not_authorize:
            data['not_authorize'] = not_authorize
        return template_render('manage.html', **data)