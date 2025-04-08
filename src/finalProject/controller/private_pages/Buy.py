from ...renderer import template_render
from ..protected_pages.get_crypto_data import GetCryptoData
from ...models.User import User
from flask import session, request, redirect, url_for
from ...helper.valitade import Validate
class Buy:
    """
    Classe responsavel por validar e gerenciar as operações de compra de criptomoedas realizadas pelo usuario
    """
    def __init__(self):
        self.data = GetCryptoData() # cria uma instancia da classe responsavel pelos dados das moedas
        self.user_data = User() # cria uma instancia da classe responsavel pelos dados do usuário
        self.valitade = Validate() # cria uma instancia responsavel pela validação
    def index(self):
        """
        Renderiza a pagina de compra onde as moedas ficarão expostas em uma tabela, no entanto o usuário
        só poderá comprar bitcoins e ethereums
        """

        #session['shop'] é usada para saber se a pagina de compra já foi aberta, caso ja tenha sido aberta,
        #não irá fazer mais requisições a API usada pra pegar o preço das moedas, pois a versão gratuita
        #da API nao permite muitas requisições por minuto
        if 'shop' not in session:

            #moedas que ficarão expostas
            cryptos = [
                'bitcoin', 'ethereum', 'aave', 'binancecoin', 'cardano',
                'ripple', 'fantom', 'dogecoin', 'solana', 'polkadot',
                'stellar', 'litecoin', 'tron', 'helium', 'uniswap'
            ]

            #pega os dados das moedas
            session['shop'] = self.data.get_crypto_data_for_buy(cryptos)

        #a session shop_coin é usada para saber qual moeda o usuário quer comprar
        if 'shop_coin' in session:
            del session['shop_coin']

        # a session authorize é usada para verificar se a compra foi realizada, e o valor será passado para o
        #javascript que exibirá um sweet alert de confirmação
        if 'authorize' in session:
            del session['authorize']
        

        return template_render('buy.html')
    
    def buy(self):        
        """
        Função que realiza a validação da compra
        """
        # pega os dados enviados do formulário
        payment = request.form.get('payment')
        four_digits_password = request.form.get('4_digits_password')
        user_cash = float(self.user_data.get_cash(user_id=session.get('user_id')))

        #verifica se esta vazio
        if not payment or not four_digits_password:
            data = {'msg': "All fields must be filled out"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #se tiver letra no campo de pagamento n passa
        if any(char.isalpha() for char in payment):
            data = {'msg': "Enter numbers only in the payment field"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #verifica se o numero tem mais de um ponto ou virgula
        if ',' in payment or '.' in payment:
            payment.replace(',', '.')

            if payment.count(".") > 1:
                data = {'msg': "Enter the payment in the format xxx.xx or xxx,xx"}
                return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
            
            try:
                float(payment)
            except ValueError:
                data = {'msg': "Enter the payment in the format xxx.xx or xxx,xx"}
                return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        # remove espaços desnecessarios
        if ' ' in payment:
            payment.strip()
            payment.replace(' ', '')

        #se o numero for maior q 9999999
        if float(payment) > 9999999:
            data = {'msg': "Enter a value less than $9999999"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #se o numero for menor q 1
        if float(payment) <= 1:
            data = {'msg': "Enter a value greater than $1"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        
        #se o valor é maior doq o valor q o usuario tem na conta
        if float(payment) > user_cash:
            data = {'msg': "Insufficient funds"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
       
        #verificação se a senha tem os 4 digitos
        if len(four_digits_password) != 4:
            data = {'msg': "Enter your four digits password"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
       
        # verifica se o usuario tem a senha de 4 digitos
        if not self.user_data.get_4_digits_pass(user_id=session.get('user_id')):
            data = {'not_authorize': "You don't have a four digits password yet, please set one to procceed with the transaction"} 
            return template_render('buy.html', **data)
        #verifica se a senha esta correta
        if not self.valitade.encryption(str(four_digits_password), self.user_data.get_4_digits_pass(session.get('user_id'))):
            data = {'msg': "Invalid password"}
            return redirect(url_for("main_routes.route_method", route_name="buy", method=session['shop_coin'], **data))
        
        #se tudo estiver correto
        self.user_data.update_cash(sit='-', user_id=session.get('user_id'), cash=float(payment))

        #pega os dados da criptomoeda a ser comprada
        if session['shop_coin'] == 'bitcoin':
            criptocurrency = self.data.get_crypto_data_for_buy(['bitcoin'])
        elif session['shop_coin'] == 'ethereum':
            criptocurrency = self.data.get_crypto_data_for_buy(['ethereum'])

        #calcula a quantidade de criptomoeda a ser comprada
        amount = float(payment)/float(criptocurrency[session['shop_coin']]['current_price'])
        
        #efetua a compra
        self.user_data.buy_crypto(user_id=session.get('user_id'), crypto_id=session['shop_coin'], amount=amount, cost=float(payment))
        
        #atualiza o saldo do usuario
        session['balance'] = self.user_data.get_cash(user_id=session.get('user_id'))

        #retorna o authorize
        data = {'authorize': 'Purchase completed successfully!'}
        return template_render('buy.html', **data)

    
    def bitcoin(self):
        """
        Renderiza o modal de compra de Bitcoin
        """
        session['shop_coin'] = 'bitcoin' #moeda a ser comprada
        if request.method == 'POST':
            return self.buy() #retorna a função de compra ao enviar o form
        
        # recupera os dados da moeda para serem exibidos no modal de compra
        data = {
            'crypto': 'bitcoin',
            'shop': session['shop']['bitcoin'],
            'modal': True
        }
        return template_render('buy.html', **data)
    
    def ethereum(self):
        """
        Renderiza o modal de compra de Ethereum
        """
        session['shop_coin'] = 'ethereum' #moeda a ser comprada
        if request.method == 'POST':
            return self.buy() #retorna a função de compra ao enviar o form
        
        # recupera os dados da moeda para serem exibidos no modal de compra
        data = {
            'crypto': 'ethereum',
            'shop': session['shop']['ethereum'],
            'modal': True
        }
        return template_render('buy.html', **data)