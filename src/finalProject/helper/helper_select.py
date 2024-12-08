from ..models.db_connection import Conn
from flask import session
import json

class Select(Conn):
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados e define variáveis de controle.

        Atributos:
            connection: Conexão com o banco de dados.
            result: Resultado da execução da consulta.
            dic: Dicionário para armazenar os parâmetros da consulta.
        """
        self.connection = Conn().connect()
        self.result = None
        self.dic = {}

    def get_result(self):
        """
        Retorna o resultado da execução da consulta.

        Retorna:
            Resultado da consulta (dependendo de como a consulta foi executada).
        """
        return self.result

    def exe_select(self, full_read, string_dic=None, close_conn=False):
        """
        Executa uma operação SELECT no banco de dados.

        Parâmetros:
            full_read (str): A consulta SELECT completa com placeholders, exemplo: 
                             "SELECT name, email FROM user_data WHERE name = %s and email = %s LIMIT %s"
            string_dic (str, opcional): String no formato JSON contendo parâmetros para a consulta.
            close_conn (bool, opcional): Se True, a conexão será fechada após a execução.

        Retorna:
            None
        """
        self.sql = full_read
        self.close_conn = close_conn

        # Se um dicionário for fornecido, tenta decodificar e processá-lo
        if string_dic is not None:
            try:
                self.dic = json.loads(string_dic)
            except json.JSONDecodeError as e:
                session["Error_con"] = "Erro ao decodificar JSON"
                return  # Encerra a execução caso ocorra erro no JSON

            # Converte valores numéricos no dicionário para inteiros, caso necessário
            int_list = ["LIMIT", "id", "offset"]
            for value in int_list:
                if value in self.dic and isinstance(self.dic[value], str) and self.dic[value].isdigit():
                    self.dic[value] = int(self.dic[value])

        # Executa a consulta
        self.execute()

    def execute(self):
        """
        Executa a consulta SQL no banco de dados.

        Retorna:
            None
        """
        try:
            cursor = self.connection.cursor()

            # Caso haja parâmetros no dicionário, executa com esses parâmetros
            if self.dic:
                dic_values = list(self.dic.values())
                cursor.execute(self.sql, dic_values)

                # Se houver limite, decide entre retornar um ou mais resultados
                if "LIMIT" in self.dic:
                    if self.dic["LIMIT"] > 1:
                        self.result = cursor.fetchall()
                    else:
                        self.result = cursor.fetchone()
                else:
                    self.result = cursor.fetchall()
            else:
                # Se não houver parâmetros, executa a consulta sem dados adicionais
                cursor.execute(self.sql)
                self.result = cursor.fetchall()

            print("Select finalizado com sucesso!")
        except Exception as e:
            # Em caso de falha, faz rollback e exibe a mensagem de erro
            self.connection.rollback()
            print(f"Erro ao realizar o select: {e}")
            session["Error_con"] = str(e)
            self.result = None
        finally:
            cursor.close()
            # Se o parâmetro 'close_conn' for True, fecha a conexão
            if self.close_conn:
                self.connection.close()
