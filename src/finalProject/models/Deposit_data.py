from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from datetime import datetime
from ..helper.helper_insert import Insert

class Deposit_data:
    """
    Classe responsavel por coletar e processar informações relacionadas ao depósito do usuário
    """
    def __init__(self):
        self.connection = Conn().connect() #conecta ao banco
        self.insert = Insert() #cria uma instancia responsavel pra inserir dados no banco

    def set_deposit(self, user_id, value, currency):
        """
        Realiza a inserção no banco do valor depositado
        """
        now = datetime.now()

        data = {
            "user_id": user_id,
            "value_deposited": value,
            "currency": currency,
            "created": now
        }
        self.insert.exe_insert(table_name='deposit', data=data)

    def get_deposit_history(self, user_id):
        """
        Pega o historico com todos os depositos feitos pelo usuario
        """
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
            
