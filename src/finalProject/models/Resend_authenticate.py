from flask import request, redirect, url_for, session
from datetime import datetime

from ..helper.helper_select import Select
from ..helper.helper_update import Update
from ..helper.valitade import Validate
from ..helper.send_email import Send_Email
from ..controller.protected_pages.Type_email import Type_email


class Resend_authenticate:
    def __init__(self):
        self.select_send = Select() 
        self.validate = Validate()
        self.send_email = Send_Email()
        self.update_sit = Update()
        self.type = Type_email()

        self.data_email = None
        self.user_authentication_id = None

    def verify_email(self, email):
        self.data_email = email
        self.select_send.exe_select("SELECT id, name, email, conf_email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{self.data_email["email"]}", "LIMIT": "1"}}', True)

        if self.validate.valitdate_email(self.data_email['email'], False):
            if self.update_conf_email():
                if self.email_resend():
                    return True
                return False
            return False
      
        return False
    
    def email_resend(self):
        email_data = self.select_send.get_result()

        if email_data:

            email_data = {"id": email_data[0], "name": email_data[1], "verify": email_data[3], "email": email_data[2]}
            
            url = "Authenticate_account/index/"
            
            # set the provider used to send the email
            self.type.get_type(email_data['email'])
            
            if self.send_email.config_email(2, email_data, url, 'code'):
                #pega o código gerado e armazena na sessao
                session['code'] = self.send_email.get_code()

                session["user_authentication_id"] = email_data["id"]
                session['type_email'] = 2

                return True

            return False
        
        session["error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False


    def update_conf_email(self):
        if self.select_send.get_result()[3] == None:
            data = {'conf_email': self.validate.encryption(str(datetime.now().date()))}
            data_where = {'id': self.select_send.get_result()[0]}
            

            self.update_sit.exe_update(data=data, table_name="user_data", data_where=data_where, operator=' =, =', close_conn=True)
            
            return self.update_sit.getResult()
        return True