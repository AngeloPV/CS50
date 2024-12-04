from ...renderer import template_render
from ..protected_pages.get_crypto_data import GetCryptoData
from ...models.User import User
from flask import session, request, redirect, url_for
from ...helper.valitade import Validate
class Buy:
    def __init__(self):
        self.data = GetCryptoData()
        self.user_data = User()
        self.valitade = Validate()
    def index(self):
        #session['shop'] é usada para saber se a pagina de compra já foi aberta, caso ja tenha sido aberta,
        #não irá fazer mais requisições a API usada pra pegar o preço das moedas, pois a versão gratuita
        #da API nao permite muitas requisições por minuto
        if 'shop' not in session:
            cryptos = [
                'bitcoin', 'ethereum', 'aave', 'binancecoin', 'cardano',
                'ripple', 'fantom', 'dogecoin', 'solana', 'polkadot',
                'stellar', 'litecoin', 'tron', 'helium', 'uniswap'
            ]

            session['shop'] = self.data.get_crypto_data_for_buy(cryptos)

        if 'shop_coin' in session:
            del session['shop_coin']
        if 'authorize' in session:
            del session['authorize']
        

        return template_render('buy.html')
    
    def buy(self):        
        payment = request.form.get('payment')
        four_digits_password = request.form.get('4_digits_password')
        user_cash = float(self.user_data.get_cash(user_id=session.get('user_id')))

        #verifica se esta vazio
        if not payment or not four_digits_password:
            data = {'msg': "Digite todos os campos"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        #se tiver letra no campo de pagamento n passa
        if any(char.isalpha() for char in payment):
            data = {'msg': "Digite apenas numeros no campo de pagamento"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #verifica se o numero tem mais de um ponto ou virgula
        if ',' in payment or '.' in payment:
            payment.replace(',', '.')

            if payment.count(".") > 1:
                data = {'msg': "Digite o pagamento no formato xxx.xx ou xxx,xx"}
                return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
            
            try:
                float(payment)
            except ValueError:
                data = {'msg': "Digite o pagamento no formato xxx.xx ou xxx,xx"}
                return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        # remove espaços desnecessarios
        if ' ' in payment:
            payment.strip()
            payment.replace(' ', '')

        #se o numero for maior q 9999999
        if float(payment) > 9999999:
            data = {'msg': "Digite um valor menor que $9999999"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #se o numero for menor q 1
        if float(payment) <= 1:
            data = {'msg': "Digite um valor maior que $1"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        
        #se o valor é maior doq o valor q o usuario tem na conta
        if float(payment) > user_cash:
            data = {'msg': "Seu saldo é insuficiente"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
       
        #verificação se a senha tem os 4 digitos
        if len(four_digits_password) != 4:
            data = {'msg': "Digite sua senha de 4 digitos"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
       
        if not self.user_data.get_4_digits_pass(user_id=session.get('user_id')):
            data = {'not_authorize': "Você  não tem uma senha de 4 digitos cadastrada, por favor cadastre uma senha para realizar a compra"}
            return template_render('buy.html', **data)
        #verifica se a senha esta correta
        if not self.valitade.encryption(str(four_digits_password), self.user_data.get_4_digits_pass(session.get('user_id'))):
            data = {'msg': "Senha inválida"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #se tudo estiver correto
        self.user_data.update_cash(sit='-', user_id=session.get('user_id'), cash=float(payment))

        if session['shop_coin'] == 'bitcoin':
            criptocurrency = self.data.get_crypto_data_for_buy(['bitcoin'])
        elif session['shop_coin'] == 'ethereum':
            criptocurrency = self.data.get_crypto_data_for_buy(['ethereum'])

        amount = float(payment)/float(criptocurrency[session['shop_coin']]['current_price'])
        
        self.user_data.buy_crypto(user_id=session.get('user_id'), crypto_id=session['shop_coin'], amount=amount, cost=float(payment))
        
        session['balance'] = self.user_data.get_cash(user_id=session.get('user_id'))
        data = {'authorize': 'Compra realizada com sucesso!'}
        return template_render('buy.html', **data)

    
    def bitcoin(self):
        session['shop_coin'] = 'bitcoin'
        if request.method == 'POST':
            return self.buy()
        data = {
            'crypto': 'bitcoin',
            'shop': session['shop']['bitcoin'],
            'modal': True
        }
        return template_render('buy.html', **data)
    
    def ethereum(self):
        session['shop_coin'] = 'ethereum'
        if request.method == 'POST':
            return self.buy()
        data = {
            'crypto': 'ethereum',
            'shop': session['shop']['ethereum'],
            'modal': True
        }
        return template_render('buy.html', **data)