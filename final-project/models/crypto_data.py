from datetime import datetime
import calendar
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py

class CryptoInfo:
    def __init__(self):
        self.connection = Conn().connect() #instacia a classe responsavel pela conexão e inicia a conexão com o banco
    
    #pega os dados de compra do usuario dos ultimos 3 meses(amount, created )
    def get_crypto_buy(self, crypto_id, user_id):
        cursor = self.connection.cursor()

        #pega o mes e o ano
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        #pega o mes inicial e o ano inicial
        start_month = current_month - 2
        start_year = current_year
        if start_month <= 0:
            start_month += 12
            start_year -= 1

        query = """
        SELECT amount, created 
        FROM buy 
        WHERE criptocurrencies_id = %s 
        AND user_id = %s 
        AND DATE_FORMAT(created, '%%Y-%%m') BETWEEN %s AND %s
        """

        #pega os valores do 3° mes
        start_date_str = f"{start_year}-{start_month:02d}"
        end_date_str = f"{current_year}-{current_month:02d}"

        cursor.execute(query, (crypto_id, user_id, start_date_str, end_date_str))
        
        data_buy = cursor.fetchall()
        cursor.close()

        return data_buy
        
    #pega o total gasto pelo usuario (criptocurrencies_id, SUM(cost))
    def get_total_spent(self, time, user_id=1):
        cursor = self.connection.cursor()

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        #se a entrada for 6 pega o valor dos ultimos 6 meses
        if time == '6':
            start_month = current_month - 5
            start_year = current_year
            if start_month <= 0:
                start_month += 12
                start_year -= 1

            last_day_current_month = calendar.monthrange(current_year, current_month)[1]

            start_date = f"{start_year}-{start_month:02d}-01"
            end_date = f"{current_year}-{current_month:02d}-{last_day_current_month}"

            query = """
            SELECT criptocurrencies_id, SUM(cost) as total_cost
            FROM buy
            WHERE user_id = %s
            AND created BETWEEN %s AND %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id, start_date, end_date))

        #pega o valor do mes atual
        elif time == '1':
            start_date = f"{current_year}-{current_month:02d}-01"
            end_date = f"{current_year}-{current_month:02d}-{calendar.monthrange(current_year, current_month)[1]}"

            query = """
            SELECT criptocurrencies_id, SUM(cost) as total_cost
            FROM buy
            WHERE user_id = %s
            AND created BETWEEN %s AND %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id, start_date, end_date))

        #pega o valor ao todo
        elif time == 'all':
            query = """
            SELECT criptocurrencies_id, SUM(cost) as total_cost
            FROM buy
            WHERE user_id = %s
            GROUP BY criptocurrencies_id
            """
            cursor.execute(query, (user_id,))

        spent_data = cursor.fetchall()
        cursor.close()

        return spent_data
    
    #pega a data da ultima compra
    def get_last_buy_date(self, user_id):
        cursor = self.connection.cursor()

        query = """SELECT created FROM buy WHERE user_id = %s ORDER BY id DESC LIMIT 1;"""
        cursor.execute(query, (user_id,))
        
        last_buy_date_row = cursor.fetchone()
        cursor.close()

        #formata a data pra ficar no modelo y/m/d
        if last_buy_date_row:
            last_buy_date = last_buy_date_row[0]
            formatted_date = last_buy_date.strftime('%Y-%m-%d')
        else:
            formatted_date = ''

        return formatted_date
    
        
    #pega as informações da ultima trade (cripto_sender_id, cripto_recipient_id, amount_sender, amount_recipient, created)
    def get_last_trade(self, user_id):
        cursor = self.connection.cursor()

        query = """SELECT cripto_sender_id, cripto_recipient_id, amount_sender, amount_recipient, created FROM 
        trades WHERE user_sender_id = %s ORDER BY id DESC LIMIT 1;"""
        cursor.execute(query, (user_id,))
        
        data = cursor.fetchall()
        cursor.close()

        return data
