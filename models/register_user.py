from ..helper.helper_insert import Insert
from ..helper.helper_select import Select
from ..helper.send_email import Send_Email
from ..helper.valitade import Validate

from datetime import datetime
from flask import session
import bcrypt # type: ignore

# Fazer o conf_email


class register_user():
    def __init__(self):
        self.insert = Insert()
        self.select = Select()
        self.send_mail = Send_Email()
        self.validate = Validate()
        self.data = None

    def addUser(self, data):
        self.data = data
        

        create = ("""
            CREATE TABLE IF NOT EXISTS user_data (
                id int(11) NOT NULL,
                name text NOT NULL,
                email varchar(220) NOT NULL,
                cpf varchar(14) NOT NULL,
                phone varchar(13) NOT NULL,
                password text NOT NULL,
                pass_4_digit varchar(4) DEFAULT NULL,
                img_name text DEFAULT NULL,
                conf_email varchar(220) NULL,
                created datetime DEFAULT current_timestamp(),
                modified datetime DEFAULT NULL
            )
        """)

        if(self.validate_camps()):
            data['password'] = self.validate.encryption(data['password'])

            data['conf_email'] = self.validate.encryption(str(datetime.now().date()))

            self.insert.exe_insert(self.data, "user_data", create, True)
            result = self.insert.getResult()

            if result:
                if(self.email()):
                    return True
                
                return False
            
            return False
        
        return False


        # where = {"id": 10}
        # self.update.exeUpdate(data, "user_data", where, ' =, =, =, =, =, >')
        # result = self.update.getResult()
        

        # self.teste.exeInsert(data, "user_data")
        # result = self.teste.getResult()
        # print(result)
        # return False

    def validate_camps(self):

        if (self.validate.valitdate_email(self.data['email']) and self.validate.valitdate_cpf(self.data['cpf']) 
            and self.validate.valitdate_phone(self.data['phone']) and self.validate.valitdate_password(self.data['password'])):
            return True
        
        return False


    def email(self):
        self.select.exe_select("SELECT id, name, email, conf_email FROM user_data WHERE cpf = %s", f'{{"cpf": "{self.data["cpf"]}"}}', True)
        email_data = self.select.get_result()

        if email_data:
            email_data = {"id": email_data[0], "name": email_data[1], "verify": email_data[3], "email": email_data[2]}
            
            url = "Authenticate_account/index/"
            
            if(self.send_mail.config_email(1, email_data, url, type='button')):
                return True

            return False
        
        session["error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False
