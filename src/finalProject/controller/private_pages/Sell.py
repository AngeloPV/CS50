from ...renderer import template_render
from ..protected_pages.get_crypto_data import GetCryptoData
from ...models.User import User
from flask import session, request, redirect, url_for
from ...helper.valitade import Validate
class Sell:
    """
    Classe responsável por gerenciar a venda de criptomoedas pelo usuário.
    """
    def __init__(self):
        self.data = GetCryptoData() # cria uma instancia da classe responsavel pelos dados das moedas
        self.user_data = User() # cria uma instancia da classe responsavel pelos dados do usuário
        self.valitade = Validate() # cria uma instancia responsavel pela validação
    def index(self):
        """
        Realiza a lógica da venda de criptomoedas, não renderiza necessáriamente uma página, embora exista
        o sell.html, esta página é usada somente para realizar as devidas operações para que seja efetuada
        a venda da respectiva moeda, sempre retornando para a página Manage
        """
        if request.method == 'POST':
            #Pega os dados do formulario
            currency = request.form.get('sell-currency')
            amount = request.form.get('sell-amount')
            password = request.form.get('4_digits_pass') 

            #Pega o saldo do usuario em bitcoin e ethereum
            user_balance = {'bitcoin': self.user_data.get_bitcoin_balance(session.get('user_id')), 
                            'ethereum': self.user_data.get_ethereum_balance(session.get('user_id'))}
            
            #Pega os dados das criptomoedas
            currency_data = self.data.get_crypto_data_for_buy(['bitcoin', 'ethereum'])

            #verifica se esta vazio
            if not currency or not amount or not password:
                data = {'msg': "All fields must be filled out", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se tem letras
            if any(char.isalpha() for char in amount):
                data = {'msg': "Enter only numbers in the sale field", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se a moeda é valida
            if currency not in ['bitcoin', 'ethereum']:
                data = {'msg': "Enter a valid currency", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica sem a quantidade a ser vendida é maior q a quantidade q o usuario possui
            if str(currency) == 'bitcoin':
                if float(amount) > float(user_balance['bitcoin']):
                    data = {'msg': "Insufficient bitcoin balance", "currency": currency}
                    return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))

            if str(currency) == 'ethereum':
                if float(amount) > float(user_balance['ethereum']):
                    data = {'msg': "Insufficient ethereum balance", "currency": currency}
                    return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se a senha tem os 4 digitos
            if len(password) != 4:
                data = {'msg': "Enter your four digits password", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se ousuario tem a senha de 4 digitos
            if not self.user_data.get_4_digits_pass(user_id=session.get('user_id')):
                data = {'not_authorize': "You don't have a 4 digits password yet, please set one to proceed with the sale"}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se a senha esta correta
            if not self.valitade.encryption(str(password), self.user_data.get_4_digits_pass(session.get('user_id'))):
                data = {'msg': "Invalid password", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #Pega o preço da respectiva moeda a ser vendida
            if str(currency) == 'bitcoin':
                price = currency_data['bitcoin']['current_price']*float(amount)
            
            if str(currency) == 'ethereum':
                price = currency_data['ethereum']['current_price']*float(amount)

            #Arredonda o preço
            price = round(price, 2)

            #Efetiva a venda
            self.user_data.update_cash(sit='+', user_id=session.get('user_id'), cash=float(price))
            self.user_data.sell_crypto(user_id=session.get('user_id'), crypto_id=currency, amount=float(amount), value=price)
            
            #Retorna para a página Manage com o valor authorize na sessão para exibir um sweet alert de sucesso
            data = {'authorize': 'Successfully sold!', 'currency': currency}
            return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))

        return template_render('sell.html')
    