from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from datetime import datetime
from ..helper.helper_insert import Insert

class Deposit_data:
    def __init__(self):
        self.connection = Conn().connect()
        self.insert = Insert()

    #deposita o valor 
    def set_deposit(self, user_id, value, currency):
        now = datetime.now()

        data = {
            "user_id": user_id,
            "value_deposited": value,
            "currency": currency,
            "created": now
        }
        self.insert.exe_insert(table_name='deposit', data=data)

    #pega o historico de depositos
    def get_deposit_history(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute("SELECT id, value_deposited, currency, created FROM deposit WHERE user_id = %s ORDER BY id DESC", (user_id,))
        data = cursor.fetchall()
        formatted_data = []

        for deposit_id, value_deposited, currency, created in data:
            # formatando a adata
            formatted_date = created.strftime('%H:%M | %Y-%m-%d')
            
            # valores padroes
            deposit_type = "Deposit"  # Tipo padrão
            status = "Confirmed"  # Status padrão

            # ajustando a sequencia dos dados
            formatted_data.append((formatted_date, deposit_id, deposit_type, value_deposited, currency, status))
            
        return formatted_data
            
