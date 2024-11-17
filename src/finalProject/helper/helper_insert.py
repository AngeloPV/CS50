from ..models.db_connection import Conn
from flask import session
from datetime import datetime

class Insert(Conn):
    def __init__(self):
        self.connection = Conn().connect()


    def getResult(self):
        return self.result

    # data: Recebe um dic com todos os dados que queria inserir na tabela
    # table_name: Recebe o nome da tabela que deseja manipular
    # create_table: Recebe a string de caso a tabela não exista, para que possa criada
    def exe_insert(self, data, table_name, create_table=None, close_conn=False):
        self.table_name = table_name
        self.close_conn = close_conn

        if (create_table is not None):
            self.create_table = create_table
        else:
            self.create_table = None

        if isinstance(data, dict):
            self.data = data

            if not self.data.get("created"):
                self.data["created"] = datetime.now()

            self.Repalce()
        else:
            self.result = False


    def Repalce(self):
        keys_data = ", ".join(self.data.keys())

        list_len = ["%s"] * len(self.data)
        placeholders = ", ".join(list_len)

        self.sql = f"INSERT INTO {self.table_name} ({keys_data}) VALUES ({placeholders})"

        self.table_insert()

    
    def table_insert(self): 
        try:
            cursor = self.connection.cursor()
            
            if self.create_table is not None :
                cursor.execute(self.create_table)

            data_values = list(self.data.values())

            cursor.execute(self.sql, data_values)

            self.connection.commit()
            print("Commit realizado com sucesso!")

            self.result = True
        except Exception as e:
        # Em caso de falha no commit, fazer rollback e exibir mensagem de erro
            self.connection.rollback()
            print(f"Erro ao fazer commit do insert: {e}")
            session["Error_con"] = str(e)
            self.result = False
        finally:
            cursor.close()
            if(self.close_conn):
                self.connection.close()
