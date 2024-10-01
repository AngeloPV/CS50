from flask import request, redirect, url_for, session

from ..helper.helper_update import Update
from ..helper.helper_select import Select
from ..helper.valitade import Validate

from datetime import datetime

class Authenticate_account_user:
    def __init__(self):
        self.update_sit = Update()
        self.select_user = Select() 
        self.validate = Validate()
        self.user_data = None

    def get_data_user(self, conf_email):

        if self.verify_conf_email(conf_email):

            self.select_user.exe_select("SELECT id FROM user_data WHERE conf_email = %s", f'{{"conf_email": "{conf_email}"}}', True)
            self.user_data = self.select_user.get_result()

            if self.user_data:
                if self.update_sit_account():
                    return True
                
                return False
            
            return False
    
        return False
    

    def update_sit_account(self):
        data = {'email_sit': 0}
        data_where = {'email_id': 1, 'user_id': self.user_data[0]}
        
        self.update_sit.exe_update(data=data, table_name="email_sit", data_where=data_where, operator=' =, =, =', close_conn=False)
        
        if self.update_sit.getResult():
            if self.update_conf_email():
                return True
            
            print('Error conf_email')
            return False
        
        return False
    
        
    def update_conf_email(self):
        data = {'conf_email': None}
        data_where = {'id': self.user_data[0]}
        
        self.update_sit.exe_update(data=data, table_name="user_data", data_where=data_where, operator=' =, =', close_conn=True)
        
        return self.update_sit.getResult()


    def verify_conf_email(self, conf_email):

        if self.validate.encryption(str(datetime.now().date()), conf_email):
            return True
        
        return False