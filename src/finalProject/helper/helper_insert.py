from ..models.db_connection import Conn
from flask import session
from datetime import datetime

class Insert(Conn):
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados.
        """
        self.connection = Conn().connect()

    def getResult(self):
        """
        Retorna o resultado da operação de insert.

        Retorna:
            bool: True se o insert foi bem-sucedido, False caso contrário.
        """
        return self.result

    def exe_insert(self, data, table_name, create_table=None, close_conn=False):
        """
        Executa uma operação de INSERT no banco de dados.

        Parâmetros:
            data (dict): Dicionário contendo os dados a serem inseridos na tabela.
            table_name (str): O nome da tabela onde os dados serão inseridos.
            create_table (str, opcional): Comando SQL para criar a tabela, se ela não existir.
            close_conn (bool, opcional): Se True, a conexão será fechada após a execução.

        Retorna:
            None
        """
        self.table_name = table_name
        self.close_conn = close_conn

        # Caso tenha sido fornecido um comando para criar a tabela, armazena
        self.create_table = create_table if create_table is not None else None

        # Verifica se 'data' é um dicionário
        if isinstance(data, dict):
            self.data = data

            # Caso o campo 'created' não exista nos dados, adiciona a data e hora atual
            if not self.data.get("created"):
                self.data["created"] = datetime.now()

            # Chama o método para formatar os dados e preparar a SQL
            self.Repalce()
        else:
            self.result = False

    def Repalce(self):
        """
        Substitui as chaves do dicionário de dados para criar a string de inserção SQL.

        Retorna:
            None
        """
        # Cria a string com os nomes das colunas
        keys_data = ", ".join(self.data.keys())

        # Cria uma lista de placeholders (%s) para cada valor
        list_len = ["%s"] * len(self.data)
        placeholders = ", ".join(list_len)

        # Monta a SQL de insert
        self.sql = f"INSERT INTO {self.table_name} ({keys_data}) VALUES ({placeholders})"

        # Chama o método para executar o insert na tabela
        self.table_insert()

    def table_insert(self):
        """
        Executa a operação de insert na tabela.

        Retorna:
            None
        """
        try:
            cursor = self.connection.cursor()

            # Caso tenha sido fornecido um comando para criar a tabela, executa-o
            if self.create_table is not None:
                cursor.execute(self.create_table)

            # Obtém os valores dos dados para serem inseridos
            data_values = list(self.data.values())

            # Executa o comando SQL de insert
            cursor.execute(self.sql, data_values)

            # Confirma as alterações no banco
            self.connection.commit()
            print("Commit realizado com sucesso!")

            # Define o resultado como True em caso de sucesso
            self.result = True
        except Exception as e:
            # Em caso de falha, faz rollback e exibe a mensagem de erro
            self.connection.rollback()
            print(f"Erro ao realizar o insert: {e}")
            session["Error_con"] = str(e)
            self.result = False
        finally:
            # Fecha o cursor após a execução
            cursor.close()
            # Se o parâmetro 'close_conn' for True, fecha a conexão
            if self.close_conn:
                self.connection.close()
