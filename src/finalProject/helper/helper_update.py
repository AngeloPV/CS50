from ..models.db_connection import Conn
from flask import session
from datetime import datetime
from itertools import chain


class Update(Conn):
    def __init__(self):
        self.connection = Conn().connect()
        self.result = None


    def getResult(self):
        return self.result

    
    # data: Recebe um dic com todos os dados que queria inserir na tabela
    # table_name: Recebe o nome da tabela que deseja manipular
    # data_where: Recebe um dic ou uma string
    # operator: Recebe um string com os operadores que cada %s vai possuir, exemplo - ' =, =, =, =, =, =, ='. TEM QUE SEGUIR ESTE FORMATO
    # onde cada %s represanta respectivamente um = ou > ou <
    def exe_update(self, data, table_name, data_where, operator=None, close_conn=False):
        self.table_name = table_name
        self.close_conn = close_conn
        self.data_where = data_where

        if operator is not None:
            self.operator = operator.split(",")

        if isinstance(data, dict):
            self.data = data

            if not self.data.get("modified"):
                self.data["modified"] = datetime.now()

            self.Repalce()
        else:
            self.result = False


    def Repalce(self):

        values_data = {}
        count = 0
        for key, value in self.data.items():
            if count < len(self.data) and key != "modified":
                values_data[key] = f'{key}{self.operator[count]} %s'

                count += 1
            elif key == "modified":
                values_data["modified"] = f'{key} = %s'

        del self.operator[:count]
        
        values_data = ", ".join(values_data.values())


        if isinstance(self.data_where, dict):

            values_data_where = {}
            count = 0

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

        self.sql_update = f"UPDATE {self.table_name} SET {values_data} WHERE {values_data_where}"

        self.update_table()

    
    def update_table(self): 
        try:
            cursor = self.connection.cursor()
            
            data_values = list(self.data.values())
            data_where = list(self.data_where.values())
  

            # Caso houver no data_where uma lista dentro de outra lista a função chain irá combinar todos os elemntos para ser apenas uma lista
            flattened_list = list(
                chain.from_iterable(
                    [x] if not isinstance(x, list) else x 
                    for x in data_where
                    )
                )

            cursor.execute(self.sql_update, data_values + flattened_list)
            self.connection.commit()
            print("Commit realizado com sucesso!")

            self.result = True
        except Exception as e:
        # Em caso de falha no commit, fazer rollback e exibir mensagem de erro
            self.connection.rollback()
            print(f"Erro ao fazer commit do update: {e}")
            session["Error_con"] = str(e) 
            self.result = False
        finally:
            cursor.close()
            if(self.close_conn):
                self.connection.close()
