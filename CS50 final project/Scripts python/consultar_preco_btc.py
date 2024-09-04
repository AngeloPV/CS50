import requests
from datetime import datetime, timedelta
import pymysql
import json

# Função para obter o preço do Bitcoin 7 dias atrás
def get_cripto_data(crypto_id):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'

    params = {
        'vs_currency': 'usd',
        'days': '30',
        'interval': 'daily'
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    price_30_days_ago = data['prices'][0][1]
    price_7_days_ago = data['prices'][-8][1]
    price_1_day_ago = data['prices'][-2][1]
    current_price = data['prices'][-1][1]
    volume_24h = data['total_volumes'][-2][1] 
    return {
        "price_30_days_ago": price_30_days_ago,
        "price_7_days_ago": price_7_days_ago,
        "price_1_day_ago": price_1_day_ago,
        "current_price": current_price,
        "volume_24h": volume_24h
    }

bitcoin_data = get_cripto_data('bitcoin')

ethereum_data = get_cripto_data('ethereum')
