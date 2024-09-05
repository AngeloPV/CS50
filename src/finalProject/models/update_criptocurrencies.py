from datetime import datetime
import json
from ..helper.helper_insert import Insert
from ..helper.helper_update import Update
from ..helper.helper_select import Select
from ..models.db_connection import Conn

class CryptoUpdate:
    def __init__(self):
        self.connection = Conn().connect()
        self.insert = Insert()
        self.update = Update()
        self.select = Select()
    
    #atualiza o banco com os valores atual das moedas
    def update_database(self, crypto_data):
        cursor = self.connection.cursor()
        #cria a tabela caso n exista
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
        #cria um json com os valores do btc ao longo dos 6 meses
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
        
        #cria um json com os valores do eth ao longo dos 6 meses
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

        # insere os dados do Bitcoin

        self.select.exe_select(full_read="SELECT * FROM criptocurrencies WHERE cripto_name = 'Bitcoin';")
        already_exists = self.select.get_result()
        
        if already_exists is None:
            data = {
                "cripto_name": "Bitcoin",
                "actual_value": crypto_data["bitcoin"]["current_price"],
                "range_value": bitcoin_range_value,
                "transaction_volume": crypto_data["bitcoin"]["volume_24h"],
                "created": datetime.now(),
                "modified": datetime.now()
            }
            self.insert.exe_insert(data=data, table_name='criptocurrencies')

        else:
            #Atualiza se ja existir
            data = {
                "actual_value": crypto_data["bitcoin"]["current_price"],
                "range_value": bitcoin_range_value,
                "transaction_volume": crypto_data["bitcoin"]["volume_24h"],
                "modified": datetime.now(),
            }
            data_where = {
                "cripto_name": 'Bitcoin'
            }
            operator = ' =, =, =, =, ='

            self.update.exe_update(data=data, table_name='criptocurrencies', data_where=data_where, operator=operator)


        #insere os dados do Ethereum
        self.select.exe_select(full_read="SELECT * FROM criptocurrencies WHERE cripto_name = 'Ethereum';")
        already_exists = self.select.get_result()
        if already_exists is None:
            data = {
                "cripto_name": "Ethereum",
                "actual_value": crypto_data["ethereum"]["current_price"],
                "range_value": ethereum_range_value,
                "transaction_volume": crypto_data["ethereum"]["volume_24h"],
                "created": datetime.now(),
                "modified": datetime.now()
            }
            self.insert.exe_insert(data=data, table_name='criptocurrencies')
        else:
            #Atualiza se ja existir

            data = {
                "actual_value": crypto_data["ethereum"]["current_price"],
                "range_value": bitcoin_range_value,
                "transaction_volume": crypto_data["ethereum"]["volume_24h"],
                "modified": datetime.now(),
            }
            data_where = {
                "cripto_name": 'Ethereum'
            }
            operator = ' =, =, =, =, ='
            self.update.exe_update(data=data, table_name='criptocurrencies', data_where=data_where, operator=operator)

