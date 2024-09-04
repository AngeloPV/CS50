import requests
import pymysql
from datetime import datetime
import json

# Função para obter os preços do Bitcoin e Ethereum e outras informações
def get_crypto_data():
    # URLs para cada período de tempo
    url_24h = 'https://api.coingecko.com/api/v3/coins/markets'
    url_7d = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    url_30d = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

    # Parâmetros para a consulta de mercado atual
    params_market = {
        'vs_currency': 'usd',
        'ids': 'bitcoin,ethereum'
    }
    
    # Parâmetros para consulta dos últimos 7 dias e 30 dias
    params_historical = {
        'vs_currency': 'usd',
        'days': '7'
    }

    response_market = requests.get(url_24h, params=params_market)
    data_market = response_market.json()

    # Obter os dados do Bitcoin e Ethereum
    bitcoin_data = next(item for item in data_market if item['id'] == 'bitcoin')
    ethereum_data = next(item for item in data_market if item['id'] == 'ethereum')

    # Obter dados históricos
    response_7d = requests.get(url_7d, params={**params_historical, 'days': '7'})
    data_7d = response_7d.json()
    price_7d = data_7d['prices'][0][1]  # Preço há 7 dias

    response_30d = requests.get(url_30d, params={**params_historical, 'days': '30'})
    data_30d = response_30d.json()
    price_30d = data_30d['prices'][0][1]  # Preço há 30 dias

    # Preparando os dados para ambos Bitcoin e Ethereum
    crypto_data = {
        "bitcoin": {
            "current_price": bitcoin_data['current_price'],
            "price_24h": bitcoin_data['price_change_percentage_24h'],
            "price_7d": price_7d,
            "price_30d": price_30d,
            "volume_24h": bitcoin_data['total_volume']
        },
        "ethereum": {
            "current_price": ethereum_data['current_price'],
            "price_24h": ethereum_data['price_change_percentage_24h'],
            "price_7d": None,  # Similar approach needed for Ethereum if 7d and 30d prices are needed
            "price_30d": None,
            "volume_24h": ethereum_data['total_volume']
        }
    }

    return crypto_data

# Função para atualizar o banco de dados
def update_database(crypto_data):
    # Configurações de conexão com o banco de dados
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'cs50'
    }

    # Conectar ao banco de dados
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Verifica se a tabela existe, se não cria
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS criptocurrencies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cripto_name VARCHAR(50),
            actual_value DECIMAL(18, 8),
            range_value JSON,
            transaction_volume DECIMAL(18, 8),
            created datetime,
            modified datetime,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Preparar range_value como JSON
    bitcoin_range_value = json.dumps({
        "24h": crypto_data["bitcoin"]["price_24h"],
        "7d": crypto_data["bitcoin"]["price_7d"],
        "30d": crypto_data["bitcoin"]["price_30d"]
    })

    ethereum_range_value = json.dumps({
        "24h": crypto_data["ethereum"]["price_24h"],
        "7d": crypto_data["ethereum"]["price_7d"],
        "30d": crypto_data["ethereum"]["price_30d"]
    })

    # Atualizar ou inserir dados do Bitcoin
    cursor.execute("SELECT * FROM criptocurrencies WHERE cripto_name = 'Bitcoin';")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO criptocurrencies (cripto_name, actual_value, range_value, transaction_volume, created, modified) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """, ('Bitcoin', crypto_data["bitcoin"]["current_price"], bitcoin_range_value, crypto_data["bitcoin"]["volume_24h"], datetime.now(), datetime.now()))
    else:
        cursor.execute("""
            UPDATE criptocurrencies 
            SET actual_value = %s, range_value = %s, transaction_volume = %s, modified = %s 
            WHERE cripto_name = 'Bitcoin';
        """, (crypto_data["bitcoin"]["current_price"], bitcoin_range_value, crypto_data["bitcoin"]["volume_24h"], datetime.now()))

    # Atualizar ou inserir dados do Ethereum
    cursor.execute("SELECT * FROM criptocurrencies WHERE cripto_name = 'Ethereum';")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO criptocurrencies (cripto_name, actual_value, range_value, transaction_volume, created, modified) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """, ('Ethereum', crypto_data["ethereum"]["current_price"], ethereum_range_value, crypto_data["ethereum"]["volume_24h"], datetime.now(), datetime.now()))
    else:
        cursor.execute("""
            UPDATE criptocurrencies 
            SET actual_value = %s, range_value = %s, transaction_volume = %s, modified = %s 
            WHERE cripto_name = 'Ethereum';
        """, (crypto_data["ethereum"]["current_price"], ethereum_range_value, crypto_data["ethereum"]["volume_24h"], datetime.now()))

    # Commit e fecha a conexão
    connection.commit()
    cursor.close()
    connection.close()

# Obtém os dados das criptomoedas
crypto_data = get_crypto_data()

# Atualiza o banco de dados com os dados
update_database(crypto_data)

print(f"Preço Atual do Bitcoin: ${crypto_data['bitcoin']['current_price']}")
print(f"Preço Atual do Ethereum: ${crypto_data['ethereum']['current_price']}")
