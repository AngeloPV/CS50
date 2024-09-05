from ..helper.helper_insert import Insert
from ..helper.helper_select import Select

from flask import session
from email_validator import validate_email, EmailNotValidError # type: ignore
from validate_docbr import CPF # type: ignore
import phonenumbers # type: ignore
from password_validator import PasswordValidator


class Validate():   
    def __init__(self):
        self.insert = Insert()
        self.select = Select()


    def valitdate_email(self, data):
        self.select.exeSelect("SELECT email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():
            try:
                email = validate_email(data, check_deliverability=False)

                return True
            except EmailNotValidError as e:

                # The exception message is human-readable explanation of why it's
                # not a valid (or deliverable) email address.
                session["Error_email"] = str(e)
                print(str(e))
                return False
        
        return False

    def valitdate_cpf(self, data):
        self.select.exeSelect("SELECT cpf FROM user_data WHERE cpf = %s LIMIT %s", f'{{"cpf": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():

            cpf = CPF()

            if cpf.validate(data):
                return True
            
            session["Error_cpf"] = "Cpf invalido!!"
            print(session["Error_cpf"])
            return False
        
        session["Error_cpf"] = "Cpf ja cadastrado em nossos sistemas!!"
        return False
        
    def valitdate_phone(self, data, region="BR"):
        self.select.exeSelect("SELECT phone FROM user_data WHERE phone = %s LIMIT %s", f'{{"phone": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():

            try:
                parserd_number = phonenumbers.parse(data, region)

                if phonenumbers.is_valid_number(parserd_number):
                    return True
            except phonenumbers.NumberParseException:
                session["Error_phone"] = "Phone invalido!!"
                return False
            
        session["Error_phone"] = "Phone ja cadastrado em nossos sistemas!!"
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
        .has().no().spaces()\
        .has().no().repeating()\
        .has().no().sequences() 

        if schema.validate(data):
            return True
        
        session["Error_password"] = "Password invalido!!"
        return False
    # def valitdate_email(self):

