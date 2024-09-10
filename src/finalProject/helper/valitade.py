from ..helper.helper_insert import Insert
from ..helper.helper_select import Select

from flask import session
from email_validator import validate_email, EmailNotValidError # type: ignore
from validate_docbr import CPF # type: ignore
import phonenumbers # type: ignore
from password_validator import PasswordValidator # type: ignore
import bcrypt # type: ignore


class Validate():   
    def __init__(self):
        self.insert = Insert()
        self.select = Select()

        if 'error_validate' in session:
            del session["error_validate"]


    def valitdate_email(self, data):
        self.select.exe_select("SELECT email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{data}", "LIMIT": "1"}}')

        
        if not self.select.get_result():
            try:
                email = validate_email(data, check_deliverability=False)

                return True
            except EmailNotValidError as e:

                # The exception message is human-readable explanation of why it's
                # not a valid (or deliverable) email address.
                session["error_validate"] = str(e)
                print(str(e))
                return False
            
        session["error_validate"] = "email ja cadastrado em nossos sistemas!!"
        return False

    def valitdate_cpf(self, data):
        self.select.exe_select("SELECT cpf FROM user_data WHERE cpf = %s LIMIT %s", f'{{"cpf": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():

            cpf = CPF()

            if cpf.validate(data):
                return True
            
            session["error_validate"] = "Cpf invalido!!"
            return False
        
        session["error_validate"] = "Cpf ja cadastrado em nossos sistemas!!"
        return False
        

    def valitdate_phone(self, data, region="BR"):
        self.select.exe_select("SELECT phone FROM user_data WHERE phone = %s LIMIT %s", f'{{"phone": "{data}", "LIMIT": "1"}}', True)
    
        if not self.select.get_result():
            print("b")
            try:
                parserd_number = phonenumbers.parse(data, region)

                if phonenumbers.is_valid_number(parserd_number):    
                    return True
                
                session["error_validate"] = "Número de telefone inválido!!"
                return False
            except phonenumbers.NumberParseException as e:
                session["error_validate"] = "Phone invalido!!"
                print(f"NumberParseException: {e}")  # Para depuração


                return False
            
        session["error_validate"] = "Phone ja cadastrado em nossos sistemas!!"
        return False

    def valitdate_password(self, data):
        schema = PasswordValidator()

        schema\
        .min(8)\
        .max(100)\
        .has().uppercase()\
        .has().lowercase()\
        .has().digits()\
        .has().no().spaces()\
        .has().symbols()\
        # .has().no().spaces()\
        # .has().no().repeating()\
        # .has().no().sequences() 

        if schema.validate(data):
            return True
        
        session["error_validate"] = "Password invalido!!"
        return False


    def validate_pass_cripto(self, user_password, db_password=None):
        if db_password is not None:
            if bcrypt.checkpw(user_password.encode("utf-8"), db_password.encode('utf-8')):
                return True
            return False
        
        return bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
