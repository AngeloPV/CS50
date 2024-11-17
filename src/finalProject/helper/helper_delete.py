from ..models.db_connection import Conn
from flask import session

class Delete(Conn):
    def __init__(self):
        self.connection = Conn().connect()


    def getResult(self):
        return self.result

    # data: Recebe um dic com todos os dados que queria inserir na tabela
    # table_name: Recebe o nome da tabela que deseja manipular
    # create_table: Recebe a string de caso a tabela não exista, para que possa criada
    def exe_delete(self, table_name, data, where_sql, close_conn=False):
        self.data = data
        self.table_name = table_name
        self.where_sql = where_sql
        self.close_conn = close_conn

        self.sql = f'DELETE FROM {table_name} WHERE {where_sql}'
        print(self.sql)

        self.delete_sql()

    def delete_sql(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute(self.sql, self.data)
            
            self.connection.commit()
            print("Delete realizado com sucesso!") 
            
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