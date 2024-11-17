from flask import url_for

from ..helper.helper_select import Select
from ..helper.valitade import Validate

from flask import session

class Login_user():
    def __init__(self):
        self.select = Select()
        self.validate = Validate()

        self.data = None
        self.result = None

    def verify_login(self, data):
        self.data = data

        self.select.exe_select("SELECT id, name, password FROM user_data WHERE email = %s OR cpf = %s OR name = %s LIMIT %s", 
                               f'{{"email": "{self.data["user"]}", "cpf": "{self.data["user"]}", "name": "{self.data["user"]}", "LIMIT": 1}}', False)
        self.result = self.select.get_result()
        
        if self.result:
            if self.validate.encryption(data['password'], self.result[2]):
                if self.verify_email_sit():
                    session['user_id'] = self.result[0]
                    print(session['user_id'])
                    return True
                
                link = url_for("main_routes.route_method", route_name="Resend_authentication_email", method="index")
                session["error_message"] = f'You need to confirm your email, request a new link: <a href="{link}" class="link" style="color: #1B263B">Confirm Email</a>'
                return False
            
            session["error_message"] = "Invalid username or password field"
            return False
        
        session["error_message"] = "Invalid username or password field"
        return False


    def verify_email_sit(self):
        self.select.exe_select("SELECT email_sit FROM email_sit WHERE email_id = %s AND user_id = %s LIMIT %s", 
                        f'{{"email_id": "2", "user_id": "{self.result[0]}", "LIMIT": 1 }}', True)
        result_email_sit = self.select.get_result()

        if result_email_sit:
            if result_email_sit[0] == 0:
                return True
            
            return False
        
        return False
    