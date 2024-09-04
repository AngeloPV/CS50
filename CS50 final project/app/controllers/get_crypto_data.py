import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.crypto_data import CryptoInfo
from app.models.update_criptocurrencies import CryptoUpdate

class GetCryptoData:
    def __init__(self):
        self.model = CryptoInfo()
        self.update = CryptoUpdate()

    #pega os dados da api dos ultimos 6 meses
    def get_cripto_data(crypto_id):
        url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
        params = {
            'vs_currency': 'usd',
            'days': '180',
            'interval': 'daily'
        }
        response = requests.get(url, params=params)
        data = response.json()

        prices = data.get('prices', [])
        total_volumes = data.get('total_volumes', [])

        # Mapeia o período para o índice
        periods = {
            "price_6_months_ago": 0,
            "price_5_months_ago": 30,
            "price_4_months_ago": 60,
            "price_3_months_ago": 90,
            "price_2_months_ago": 120,
            "price_1_month_ago": 150,
            "price_7_days_ago": -8,
            "price_1_day_ago": -2,
            "current_price": -1
        }

        def get_price_at_index(index, default=None):
            """Retorna o preço no índice especificado ou um valor padrão."""
            try:
                return prices[index][1]
            except IndexError:
                return default

        # Preenche os valores dos preços usando o mapeamento
        price_data = {key: get_price_at_index(index) for key, index in periods.items()}

        # Volume nas últimas 24 horas
        volume_24h = get_price_at_index(-2, default=None) if len(total_volumes) > 1 else None

        # Adiciona o volume 24h aos dados
        price_data["volume_24h"] = volume_24h

        return price_data

    #chama a funcao no valor referente a moeda
    crypto_data = {
        "bitcoin": get_cripto_data('bitcoin'),
        "ethereum": get_cripto_data('ethereum')
    }
    #atualiza o banco com o valor atual das moedas
    def do_update_database(self):
        self.update.update_database(self.crypto_data)  

    #pega o volume de transação nas ultimas 24hrs
    def get_volume(self, crypto_name):
        return self.crypto_data[crypto_name]['volume_24h']

    #pega os dados de compra do usuario (amount, created )
    def get_crypto_buy(self, crypto_id, user_id):
        return self.model.get_crypto_buy(crypto_id=crypto_id, user_id=user_id)

    #pega o total gasto pelo usuario (criptocurrencies_id, SUM(cost))
    def get_total_spent(self, user_id, time): 
        return self.model.get_total_spent(time=time, user_id=user_id)

    #pega a data da ultima compra (created)
    def get_last_buy_date(self, user_id):
        return self.model.get_last_buy_date(user_id=user_id)

    #pega as informações da ultima trade (cripto_sender_id, cripto_recipient_id, amount_sender, amount_recipient, created)
    def get_last_trade_data(self, user_id):
        return self.model.get_last_trade(user_id=user_id)
