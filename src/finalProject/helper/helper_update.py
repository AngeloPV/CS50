from ..models.db_connection import Conn
from flask import session
from datetime import datetime
from itertools import chain

class Update(Conn):
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e define a variável de controle.

        Atributos:
            connection: Conexão com o banco de dados.
            result: Resultado da execução do comando de atualização.
        """
        self.connection = Conn().connect()
        self.result = None

    def getResult(self):
        """
        Retorna o resultado da execução do comando de atualização.

        Retorna:
            bool: Resultado da execução (True se bem-sucedido, False se falhou).
        """
        return self.result

    def exe_update(self, data, table_name, data_where, operator=None, close_conn=False):
        """
        Executa uma operação UPDATE no banco de dados.

        Parâmetros:
            data (dict): Dicionário com os dados a serem atualizados.
            table_name (str): Nome da tabela onde a atualização será realizada.
            data_where (dict ou str): Condições de filtro para o comando WHERE.
            operator (str, opcional): Operadores para os placeholders (%s) no formato de string. Exemplo: ' =, =, ='.
            close_conn (bool, opcional): Se True, a conexão será fechada após a execução.

        Retorna:
            None
        """
        self.table_name = table_name
        self.close_conn = close_conn
        self.data_where = data_where

        # Se operadores forem fornecidos, divide a string para utilizá-los
        if operator is not None:
            self.operator = operator.split(",")

        # Verifica se os dados são um dicionário e adiciona a data de modificação
        if isinstance(data, dict):
            self.data = data
            if not self.data.get("modified"):
                self.data["modified"] = datetime.now()

            self.Repalce()  # Chama a função para construir a query de UPDATE
        else:
            self.result = False

    def Repalce(self):
        """
        Constrói a consulta SQL para o comando UPDATE com base nos dados e condições fornecidas.

        Retorna:
            None
        """
        values_data = {}
        count = 0

        # Constrói os placeholders e associa cada valor da atualização
        for key, value in self.data.items():
            if count < len(self.data) and key != "modified":
                values_data[key] = f'{key}{self.operator[count]} %s'
                count += 1
            elif key == "modified":
                values_data["modified"] = f'{key} = %s'

        # Remove os operadores usados
        del self.operator[:count]
        
        # Junta os placeholders para a consulta
        values_data = ", ".join(values_data.values())

        # Constrói a parte do WHERE da consulta
        if isinstance(self.data_where, dict):
            values_data_where = {}
            count = 0

            # Constrói as condições de WHERE com base nos dados fornecidos
            for key, value in self.data_where.items():
                if count < len(self.data_where):
                    if self.operator[count] == ' IN' and isinstance(value, list):
                        placeholders = ', '.join(['%s'] * len(value))
                        values_data_where[key] = f'{key}{self.operator[count]} ({placeholders})'
                    else:
                        values_data_where[key] = f'{key}{self.operator[count]} %s'
                    count += 1

            values_data_where = " AND ".join(values_data_where.values())

        elif isinstance(self.data_where, str):
            values_data_where = self.data_where

        # Constrói a consulta final de UPDATE
        self.sql_update = f"UPDATE {self.table_name} SET {values_data} WHERE {values_data_where}"

        self.update_table()  # Chama a função para executar a consulta

    def update_table(self):
        """
        Executa a consulta UPDATE no banco de dados.

        Retorna:
            None
        """
        try:
            cursor = self.connection.cursor()

            # Obtém os valores dos dados e da condição WHERE
            data_values = list(self.data.values())
            data_where = list(self.data_where.values())
  
            # Caso haja listas dentro de data_where, a função 'chain' irá achatar para garantir que os valores sejam passados corretamente
            flattened_list = list(
                chain.from_iterable(
                    [x] if not isinstance(x, list) else x 
                    for x in data_where
                )
            )

            # Executa a consulta de UPDATE com os valores
            cursor.execute(self.sql_update, data_values + flattened_list)
            self.connection.commit()
            print("Commit realizado com sucesso!")

            self.result = True
        except Exception as e:
            # Em caso de falha, faz rollback e exibe a mensagem de erro
            self.connection.rollback()
            print(f"Erro ao realizar o update: {e}")
            session["Error_con"] = str(e) 
            self.result = False
        finally:
            cursor.close()
            # Se o parâmetro 'close_conn' for True, fecha a conexão
            if self.close_conn:
                self.connection.close()
