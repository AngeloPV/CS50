# conecta ao bd
import pymysql

class Conn:
    """
    Classe responsável por estabelecer a conexão e com o banco de dados
    """
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'cs50'
        }

    def connect(self):
        """
        Realiza a conexão com o banco de dados
        """
        return pymysql.connect(**self.db_config)
