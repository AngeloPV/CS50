from .helper_insert import Insert
from .helper_select import Select

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
    
        if 'error_validate' not in session:
            session['error_validate'] = {}


    def valitdate_email(self, data, cond):
        self.select.exe_select("SELECT email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{data}", "LIMIT": "1"}}')

        print(self.select.get_result())
        if not self.select.get_result() and cond == True:
            session["error_validate"]['email'] = "Email not registered in our systems"
            return False
 
        if cond == False:
            try:
                email = validate_email(data, check_deliverability=False)

                return True
            except EmailNotValidError as e:

                # The exception message is human-readable explanation of why it's
                # not a valid (or deliverable) email address.
                session["error_validate"]['email'] = str(e)
                print(str(e))
                return False

        session["error_validate"]['email'] = "Email already registered in our systems!"
        return False

    def valitdate_cpf(self, data):
        self.select.exe_select("SELECT cpf FROM user_data WHERE cpf = %s LIMIT %s", f'{{"cpf": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():

            cpf = CPF()

            if cpf.validate(data):
                return True
            
            session["error_validate"]['cpf'] = "The CPF entered is invalid. Please check the number you entered and try again."
            return False
        
        session["error_validate"]['cpf'] = "CPF already registered in our systems!"
        return False
        

    def valitdate_phone(self, data, region="BR"):
        self.select.exe_select("SELECT phone FROM user_data WHERE phone = %s LIMIT %s", f'{{"phone": "{data}", "LIMIT": "1"}}')
    
        if not self.select.get_result():
            try:
                parserd_number = phonenumbers.parse(data, region)

                if phonenumbers.is_valid_number(parserd_number):    
                    return True
                
                session["error_validate"]['phone'] = "The telephone number provided is invalid. Please check the format and try again."
                return False
            except phonenumbers.NumberParseException as e:
                session["error_validate"]['phone'] = "The telephone number provided is invalid. Please check the format and try again."
                print(f"NumberParseException: {e}")  # Para depuração


                return False
            
        session["error_validate"]['phone'] = "Phone number already registered in our systems."
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

        if schema.validate(data):
            return True
        
        session["error_validate"]["password"] = "Password invalid! Must be between 8 and 50 characters, include upper and lower case letters, numbers, symbols and not contain spaces."
        return False


    def encryption(self, user_password, db_password=None):
        if db_password is not None:
            if "_" in db_password:
                hased_db = db_password.replace('_', '/')
            else:
                hased_db = db_password

            if bcrypt.checkpw(user_password.encode("utf-8"), hased_db.encode('utf-8')):
                return True
            
            session["error_validate"] = "The password don't match!"
            return False
        
        password_hased = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        return password_hased.decode('utf-8').replace('/', '_')