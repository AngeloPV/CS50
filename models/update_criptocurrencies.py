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
    
    # Atualiza o banco com os valores atuais das criptomoedas
    def update_database(self, crypto_data):
        cursor = self.connection.cursor()

        #cria a tabela uma única vez se ela não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS criptocurrencies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cripto_name VARCHAR(50) NOT NULL,
                actual_value DECIMAL(20, 8),
                range_value JSON,
                transaction_volume DECIMAL(20, 8),
                created DATETIME,
                modified DATETIME,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP     
            )
        """)

        #mapeia os dados para Bitcoin e Ethereum
        for crypto_name, crypto_key in [("Bitcoin", "bitcoin"), ("Ethereum", "ethereum")]:
            range_value = json.dumps({
                "24h": crypto_data[crypto_key]["price_1_day_ago"],
                "7d": crypto_data[crypto_key]["price_7_days_ago"],
                "1m": crypto_data[crypto_key]["price_1_month_ago"],
                "2m": crypto_data[crypto_key]["price_2_months_ago"],
                "3m": crypto_data[crypto_key]["price_3_months_ago"],
                "4m": crypto_data[crypto_key]["price_4_months_ago"],
                "5m": crypto_data[crypto_key]["price_5_months_ago"],
                "6m": crypto_data[crypto_key]["price_6_months_ago"],
            })

            #verifica se a criptomoeda já existe no banco
            self.select.exe_select(f"SELECT * FROM criptocurrencies WHERE cripto_name = '{crypto_name}';")
            already_exists = self.select.get_result()

            data = {
                "cripto_name": crypto_name,
                "actual_value": crypto_data[crypto_key]["current_price"],
                "range_value": range_value,
                "modified": datetime.now(),
            }

            if already_exists is None:
                data["created"] = datetime.now()
                self.insert.exe_insert(data=data, table_name='criptocurrencies')
            else:
                #atualiza os dados se já existir
                data_where = {"cripto_name": crypto_name}
                operator = ' =, =, =, =, ='
                self.update.exe_update(data=data, table_name='criptocurrencies', data_where=data_where, operator=operator)
