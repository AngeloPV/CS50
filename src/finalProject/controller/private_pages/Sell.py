from ...renderer import template_render
from ..protected_pages.get_crypto_data import GetCryptoData
from ...models.User import User
from flask import session, request, redirect, url_for
from ...helper.valitade import Validate
class Sell:
    def __init__(self):
        self.data = GetCryptoData()
        self.user_data = User()
        self.valitade = Validate()
    def index(self):
        if request.method == 'POST':
            currency = request.form.get('sell-currency')
            amount = request.form.get('sell-amount')
            password = request.form.get('4_digits_pass') 

            user_balance = {'bitcoin': self.user_data.get_bitcoin_balance(session.get('user_id')), 
                            'ethereum': self.user_data.get_ethereum_balance(session.get('user_id'))}
            
            currency_data = self.data.get_crypto_data_for_buy(['bitcoin', 'ethereum'])
            #verifica se esta vazio
            if not currency or not amount or not password:
                data = {'msg': "Digite todos os campos", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se tem letras
            if any(char.isalpha() for char in amount):
                data = {'msg': "Digite apenas numeros no campo de pagamento", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se a moeda é valida
            if currency not in ['bitcoin', 'ethereum']:
                data = {'msg': "Digite uma moeda valida", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica sem a quantidade a ser vendida é maior q a quantidade q o usuario possui
            if str(currency) == 'bitcoin':
                if float(amount) > float(user_balance['bitcoin']):
                    data = {'msg': "Seu saldo de bitcoin é insuficiente", "currency": currency}
                    return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))

            if str(currency) == 'ethereum':
                if float(amount) > float(user_balance['ethereum']):
                    data = {'msg': "Seu saldo de ethereum é insuficiente", "currency": currency}
                    return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se a senha tem os 4 digitos
            if len(password) != 4:
                data = {'msg': "Digite a sua senha de 4 digitos", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            #verifica se ousuario tem a senha de 4 digitos
            if not self.user_data.get_4_digits_pass(user_id=session.get('user_id')):
                data = {'not_authorize': "Você  não tem uma senha de 4 digitos cadastrada, por favor cadastre uma senha para realizar a compra"}
                return template_render('sell.html', **data)
            
            #verifica se a senha esta correta
            if not self.valitade.encryption(str(password), self.user_data.get_4_digits_pass(session.get('user_id'))):
                data = {'msg': "Senha inválida", "currency": currency}
                return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))
            
            if str(currency) == 'bitcoin':
                price = currency_data['bitcoin']['current_price']*float(amount)
            
            if str(currency) == 'ethereum':
                price = currency_data['ethereum']['current_price']*float(amount)
            #efetiva a venda
            price = round(price, 2)
            self.user_data.update_cash(sit='+', user_id=session.get('user_id'), cash=float(price))
            self.user_data.sell_crypto(user_id=session.get('user_id'), crypto_id=currency, amount=float(amount), value=price)
            
            data = {'authorize': 'Venda realizada com sucesso!'}
            return redirect(url_for("main_routes.route_method", route_name="manage", method='index', **data))

        return template_render('sell.html')
    