# conecta ao bd
import pymysql

class Conn:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'cs50'
        }

    def connect(self):
        return pymysql.connect(**self.db_config)
