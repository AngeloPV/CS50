from ..models.db_connection import Conn
from flask import session

class Delete(Conn):
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados.
        """
        self.connection = Conn().connect()

    def getResult(self):
        """
        Retorna o resultado da operação de delete.
        """
        return self.result

    def exe_delete(self, table_name, data, where_sql, close_conn=False):
        """
        Executa uma operação de DELETE no banco de dados.

        Parâmetros:
            table_name (str): O nome da tabela a ser manipulada.
            data (dict): Os dados a serem passados para a execução do DELETE.
            where_sql (str): A cláusula WHERE para filtrar os registros.
            close_conn (bool): Se True, a conexão será fechada após a execução.
        """
        self.data = data
        self.table_name = table_name
        self.where_sql = where_sql
        self.close_conn = close_conn

        self.sql = f"DELETE FROM {table_name} WHERE {where_sql}"
        print(self.sql)

        self.delete_sql()

    def delete_sql(self):
        """
        Executa a consulta DELETE no banco de dados.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(self.sql, self.data)
            self.connection.commit()
            print("Delete realizado com sucesso!") 
            self.result = True
        except Exception as e:
            # Em caso de falha no commit, faz rollback e exibe mensagem de erro
            self.connection.rollback()
            print(f"Erro ao realizar o DELETE: {e}")
            session["Error_con"] = str(e)
            self.result = False
        finally:
            cursor.close()
            if self.close_conn:
                self.connection.close()
