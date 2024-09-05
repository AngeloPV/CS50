from ..helper.helper_insert import Insert
from ..helper.helper_select import Select
from ..helper.send_email import Send_Email
from ..helper.valitade import Validate

from flask import session

class register_user():
    def __init__(self):
        self.insert = Insert()
        self.select = Select()
        self.send_mail = Send_Email()
        self.validate = Validate()

    def addUser(self, data):
        # self.validate.valitdate_email(data['email'])
        self.validate.valitdate_cpf(data['cpf'])

        # create = ("""
        #     CREATE TABLE IF NOT EXISTS user_data (
        #         id int(11) NOT NULL,
        #         name text NOT NULL,
        #         email varchar(220) NOT NULL,
        #         cpf varchar(14) NOT NULL,
        #         phone varchar(13) NOT NULL,
        #         password text NOT NULL,
        #         pass_4_digit varchar(4) DEFAULT NULL,
        #         img_name text DEFAULT NULL,
        #         created datetime DEFAULT current_timestamp(),
        #         modified datetime DEFAULT NULL
        #     )
        # """)
        
        # self.insert.exeInsert(data, "user_data", True, create)
        # result = self.insert.getResult()

        # if result:
        #     if(self.Email(data)):
        #         return True
            
        #     return False
        
        return False
        # self.read.full_read("SELECT name, email FROM user_data WHERE name = %s and email = %s LIMIT %s", f'{{"name": "{data["name"]}", "email": "{data["email"]}", "LIMIT": "3"}}')

        # self.read.full_read("SELECT * FROM user_data")
        # result = self.read.get_result()

        # where = {"id": 10}
        # self.update.exeUpdate(data, "user_data", where, ' =, =, =, =, =, >')
        # result = self.update.getResult()
        
        # where = {"id": 5}
        # self.update.exeUpdate(data, "user_data", where, ' =, =, =, =, =, <', True)
        # result = self.update.getResult()

        # self.teste.exeInsert(data, "user_data")
        # result = self.teste.getResult()
        # print(result)
        # return False

    def Email(self, data):
        self.select.exeSelect("SELECT id, name, email FROM user_data WHERE cpf = %s", f'{{"cpf": "{data["cpf"]}"}}', True)
        email_data = self.select.get_result()
        
        if email_data:
            email_data = {"name": email_data[1], "verify": email_data[0], "email": email_data[2]}
            
            url = "teste/teste/"
            
            if(self.send_mail.configEmail(1, email_data, url)):
                return True

            return False
        
        session["Error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False