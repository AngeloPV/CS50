from datetime import datetime
import json

from models.db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py

class CryptoUpdate:
    def __init__(self):
        self.connection = Conn().connect()

    def update_database(self, crypto_data):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS criptocurrencies (
                id int AUTO_INCREMENT PRIMARY KEY,
                cripto_name varchar(50) NOT NULL,
                actual_value DECIMAL(20, 8),
                range_value JSON,
                transaction_volume DECIMAL(20, 8),
                created datetime,
                modified datetime,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP     
            )
        """)

        bitcoin_range_value = json.dumps({
            "24h": crypto_data["bitcoin"]["price_1_day_ago"],
            "7d": crypto_data["bitcoin"]["price_7_days_ago"],
            "1m": crypto_data["bitcoin"]["price_1_month_ago"],
            "2m": crypto_data["bitcoin"]["price_2_months_ago"],
            "3m": crypto_data["bitcoin"]["price_3_months_ago"],
            "4m": crypto_data["bitcoin"]["price_4_months_ago"],
            "5m": crypto_data["bitcoin"]["price_5_months_ago"],
            "6m": crypto_data["bitcoin"]["price_6_months_ago"],
        })
            
        ethereum_range_value = json.dumps({
            "24h": crypto_data["ethereum"]["price_1_day_ago"],
            "7d": crypto_data["ethereum"]["price_7_days_ago"],
            "1m": crypto_data["ethereum"]["price_1_month_ago"],
            "2m": crypto_data["ethereum"]["price_2_months_ago"],
            "3m": crypto_data["ethereum"]["price_3_months_ago"],
            "4m": crypto_data["ethereum"]["price_4_months_ago"],
            "5m": crypto_data["ethereum"]["price_5_months_ago"],
            "6m": crypto_data["ethereum"]["price_6_months_ago"],
        })

        # Atualiza ou insere os dados do Bitcoin
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

        # Atualiza ou insere os dados do Ethereum
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

        self.connection.commit()
        cursor.close()
