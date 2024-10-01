from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from ..helper.helper_select import Select
class User:
    def __init__(self):
        self.connection = Conn().connect() 
        self.select = Select()
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
        self.select.exe_select("SELECT img_name FROM user_data WHERE id = %s", 
                               f'{{"id": "{user_id}"}}', False)
        img = self.select.get_result()     
        return img[0]