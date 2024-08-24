import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.crypto_data import CryptoInfo
from models.update_database import CryptoUpdate

class CryptoController:
    def __init__(self):
        self.model = CryptoInfo()
        self.update = CryptoUpdate()

def get_cripto_data(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '180',
        'interval': 'daily'
    }
    response = requests.get(url, params=params)
    data = response.json()

    price_6_months_ago = price_5_months_ago = price_4_months_ago = price_3_months_ago = price_2_months_ago = price_1_month_ago = None
    price_7_days_ago = price_1_day_ago = current_price = None
    volume_24h = None

    try:
        prices = data.get('prices', [])
        total_volumes = data.get('total_volumes', [])

        if len(prices) > 0:
            price_6_months_ago = prices[0][1]
        if len(prices) > 30:
            price_5_months_ago = prices[30][1]
        if len(prices) > 60:
            price_4_months_ago = prices[60][1]
        if len(prices) > 90:
            price_3_months_ago = prices[90][1]
        if len(prices) > 120:
            price_2_months_ago = prices[120][1]
        if len(prices) > 150:
            price_1_month_ago = prices[150][1]
        if len(prices) > 8:
            price_7_days_ago = prices[-8][1]
        if len(prices) > 2:
            price_1_day_ago = prices[-2][1]
        if len(prices) > 0:
            current_price = prices[-1][1]
        if len(total_volumes) > 1:
            volume_24h = total_volumes[-2][1]

    except (IndexError, KeyError, TypeError) as e:
        print(f"Erro ao processar os dados: {e}")

    return {
        "price_6_months_ago": price_6_months_ago,
        "price_5_months_ago": price_5_months_ago,
        "price_4_months_ago": price_4_months_ago,
        "price_3_months_ago": price_3_months_ago,
        "price_2_months_ago": price_2_months_ago,
        "price_1_month_ago": price_1_month_ago,
        "price_7_days_ago": price_7_days_ago,
        "price_1_day_ago": price_1_day_ago,
        "current_price": current_price,
        "volume_24h": volume_24h
    }

crypto_data = {
    "bitcoin": get_cripto_data('bitcoin'),
    "ethereum": get_cripto_data('ethereum')
}

def do_update_database():
    controller = CryptoController()  
    controller.update.update_database(crypto_data)  

def get_volume(crypto_name):
    return crypto_data[crypto_name]['volume_24h']

def get_crypto_buy(crypto_id, user_id):
    crypto_model_instance = CryptoInfo() 
    return crypto_model_instance.get_crypto_buy(crypto_id=crypto_id, user_id=user_id)

def get_total_spent(user_id, time):
    crypto_model_instance = CryptoInfo() 
    return crypto_model_instance.get_total_spent(time=time, user_id=user_id)

def get_last_buy_date(user_id):
    crypto_model_instance = CryptoInfo() 
    return crypto_model_instance.get_last_buy_date(user_id=user_id)

def get_last_trade_data(user_id):
    crypto_model_instance = CryptoInfo() 
    return crypto_model_instance.get_last_trade(user_id=user_id)
