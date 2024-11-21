from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from ..helper.helper_select import Select
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update
from ..helper.helper_insert import Insert
from datetime import datetime
class User:
    def __init__(self):
        self.connection = Conn().connect() 
        self.select = Select()
        self.delete = Delete()
        self.update = Update()
        self.insert = Insert()
        self.result = None

    #define a senha de 4 ditos do usario
    def set_4_digits_pass(self, password, user_id):
        cursor = self.connection.cursor()

        query = """UPDATE user_data SET pass_4_digit = %s WHERE id = %s"""
        cursor.execute(query, (password, user_id))
        self.connection.commit()
        cursor.close()

    def get_4_digits_pass(self, user_id):
        self.select.exe_select("SELECT pass_4_digit FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        password = self.select.get_result()     
        if not password:
            return False
        return password[0]
        
    
    def set_profile_image(self, img, user_id):
        cursor = self.connection.cursor()

        query = """UPDATE user_data SET img_name = %s WHERE id = %s"""
        cursor.execute(query, (img, user_id))
        self.connection.commit()
        cursor.close()
    
    def get_profile_image(self, user_id):
        self.select.exe_select("SELECT img_name FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        img = self.select.get_result()     
        return img[0]
    
    def get_user_name(self, user_id):
        self.select.exe_select("SELECT name FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        nome_completo = self.select.get_result() 
        nomes = nome_completo[0].split()    
        return nomes
    
    def get_user_email(self, user_id):
        self.select.exe_select("SELECT email FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        email = self.select.get_result() 
        return email[0]
    
    def get_user_phone(self, user_id):
        self.select.exe_select("SELECT phone FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        phone = self.select.get_result() 
        return phone[0]
    
    def get_theme(self, user_id):
        self.select.exe_select("SELECT theme FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        theme = self.select.get_result() 
        return theme[0]
    
    def set_theme(self, user_id, theme):
        self.update.exe_update(data={"theme": theme}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = True)
        return True
    
    def get_language(self, user_id):
        self.select.exe_select("SELECT language FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        language = self.select.get_result() 
        return language[0]
    
    def delete_account(self, user_id):
        self.delete.exe_delete(table_name="user_data", where_sql="id = %s", data=(user_id,), 
                               close_conn = True)
        
        return self.delete.getResult()
    
    #parte do dinheiro, usar a sit como + pra ganho e - pra perda
    def update_cash(self, sit, user_id, cash):
        cursor = self.connection.cursor()
        
        if sit == '+':
            query = """INSERT INTO user_cash
                    VALUES ('',%s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE 
                    cash = cash + %s,
                    modified = NOW();"""
        else:
            query = """INSERT INTO user_cash
                    VALUES ('',%s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE 
                    cash = cash - %s,
                    modified = NOW();"""
            
        cursor.execute(query, (user_id, cash, cash))
        self.connection.commit()
        cursor.close()
        return True
    
    def get_cash(self, user_id):
        self.select.exe_select("SELECT cash FROM user_cash WHERE user_id = %s LIMIT %s", 
                               f'{{"user_id": "{user_id}", "LIMIT": 1}}', False)
        cash = self.select.get_result() 
        if not cash:
            return 0
        return cash[0]
    
    def buy_crypto(self, user_id, crypto_id, amount, cost):
        cursor = self.connection.cursor()

        if crypto_id == 'bitcoin':
            crypto_id = 1
            query = """INSERT INTO user_btc
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount + %s,
                modified = NOW();""" 

        elif crypto_id == 'ethereum':
            crypto_id = 2 
            query = """INSERT INTO user_eth
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount + %s,
                modified = NOW();""" 

        cursor.execute(query, (user_id, amount, amount))
        self.connection.commit()
        cursor.close()

        now = datetime.now()

        data = {
            "id": '',
            "user_id": user_id,
            "criptocurrencies_id": crypto_id,
            "amount": amount,
            "cost": cost,
            "created": now
        }
        self.insert.exe_insert(table_name='buy', data=data)