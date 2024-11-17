from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from ..helper.helper_select import Select
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update
class User:
    def __init__(self):
        self.connection = Conn().connect() 
        self.select = Select()
        self.delete = Delete()
        self.update = Update()
        self.result = None

    #define a senha de 4 ditos do usario
    def set_4_digits_pass(self, password, user_id):
        cursor = self.connection.cursor()

        query = """UPDATE user_data SET pass_4_digit = %s WHERE id = %s"""
        cursor.execute(query, (password, user_id))
        self.connection.commit()
        cursor.close()

    def get_4_digits_pass(self, user_id):
        cursor = self.connection.cursor()

        query = """SELECT pass_4_digit FROM user_data WHERE id = %s"""
        cursor.execute(query, (user_id))
        
        password = cursor.fetchone()
        cursor.close()

        if password is None or password[0] is None:
            return False
        return True
    
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