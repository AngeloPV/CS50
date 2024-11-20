from ...renderer import template_render
from ..protected_pages.get_crypto_data import GetCryptoData
from flask import session
class Buy:
    def __init__(self):
        self.data = GetCryptoData()
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
        
        return template_render('buy.html')
    
    def bitcoin(self):
        data = {
            'shop': session['shop']['bitcoin'],
            'modal': True
        }
        return template_render('buy.html', **data)
    
    def ethereum(self):
        data = {
            'shop': session['shop']['ethereum'],
            'modal': True
        }
        return template_render('buy.html', **data)