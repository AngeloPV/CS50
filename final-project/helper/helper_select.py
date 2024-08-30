from ..models.db_connection import Conn
from flask import session
import json

class Select(Conn):
    def __init__(self):
        self.connection = Conn().connect()
        self.result = None
        self.dic = {}


    def get_result(self):
        return self.result

    # full read: Recebe todo o select exemplo - "SELECT name, email FROM user_data WHERE name = %s and email = %s LIMIT %s"
    # string_dic: Recebe uma f-string no formato de dicionario exemplo - f'{{"name": "{data["name"]}", "email": "{data["email"]}", "LIMIT": "3"}}')
    def exeSelect(self, full_read, string_dic=None, close_conn=False):
        self.sql = full_read

        self.close_conn = close_conn

        if string_dic is not None:
                self.dic = json.loads(string_dic)

                if "LIMIT" not in self.dic or not self.dic["LIMIT"]:
                    self.sql = f"{self.sql} LIMIT 1"

                
                int_list = ["LIMIT", "id", "offset"]

                for value in int_list:
                    print(value)
                    if value in self.dic and isinstance(self.dic[value], str) and self.dic[value].isdigit():
                        self.dic[value] = int(self.dic[value])


                # for i in int_list:
                #     if int_list[i] in dict
                # elif "LIMIT" in self.dic and isinstance(self.dic["LIMIT"], str) and self.dic["LIMIT"].isdigit():
                #     self.dic["LIMIT"] = int(self.dic["LIMIT"])

        self.table_select()

    
    def table_select(self): 
        try:
            cursor = self.connection.cursor()
            
            if self.dic:
                dic_values = list(self.dic.values())

                cursor.execute(self.sql, dic_values)

                
                if "LIMIT" in self.dic:
                    self.result = cursor.fetchall()
                else:
                    self.result = cursor.fetchone()
            else:
                cursor.execute(self.sql)

                self.result = cursor.fetchall()

                
            print("Select finalizdo com sucesso!")
        except Exception as e:
        # Em caso de falha no commit, fazer rollback e exibir mensagem de erro
            self.connection.rollback()
            print(f"Erro ao fazer select: {e}")
            session["Error_con"] = str(e)
            self.result = None
        finally:
            cursor.close()
            if(self.close_conn):
                self.connection.close()
