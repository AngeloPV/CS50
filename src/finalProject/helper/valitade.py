from .helper_insert import Insert
from .helper_select import Select

from flask import session
from email_validator import validate_email, EmailNotValidError  # type: ignore
from validate_docbr import CPF  # type: ignore
import phonenumbers  # type: ignore
from password_validator import PasswordValidator  # type: ignore
import bcrypt  # type: ignore


class Validate():
    """
    Classe responsável pela validação de dados como e-mail, CPF, telefone, senha e criptografia de senha.
    Também realiza a verificação de duplicidade no banco de dados.

    Atributos:
        insert (Insert): Instância da classe Insert para inserções no banco de dados.
        select (Select): Instância da classe Select para consultas ao banco de dados.
    """

    def __init__(self):
        """
        Inicializa as instâncias necessárias e limpa a sessão de erros de validação.
        """
        self.insert = Insert()
        self.select = Select()

        # Limpa a sessão de erros, se existir
        if 'error_validate' in session:
            del session["error_validate"]

        # Se não existir, inicializa a sessão de erros
        if 'error_validate' not in session:
            session['error_validate'] = {}

    def validate_email(self, data, cond):
        """
        Valida o e-mail fornecido. Verifica se ele já está registrado no banco de dados ou se é válido.

        Parâmetros:
            data (str): O e-mail a ser validado.
            cond (bool): Condição para verificar se o e-mail está registrado.

        Retorna:
            bool: Retorna True se o e-mail for válido ou não registrado, caso contrário False.
        """
        self.select.exe_select("SELECT email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result() and cond == True:
            session["error_validate"]['email'] = "Email not registered in our systems"
            return False

        if cond == False:
            try:
                # Valida o e-mail utilizando a biblioteca email_validator
                email = validate_email(data, check_deliverability=False)
                return True
            except EmailNotValidError as e:
                # Se o e-mail não for válido, armazena a mensagem de erro na sessão
                session["error_validate"]['email'] = str(e)
                print(str(e))
                return False

        # E-mail já registrado
        session["error_validate"]['email'] = "Email already registered in our systems!"
        return False

    def validate_cpf(self, data):
        """
        Valida o CPF fornecido. Verifica se o CPF é válido e se já está registrado no banco de dados.

        Parâmetros:
            data (str): O CPF a ser validado.

        Retorna:
            bool: Retorna True se o CPF for válido e não registrado, caso contrário False.
        """
        self.select.exe_select("SELECT cpf FROM user_data WHERE cpf = %s LIMIT %s", f'{{"cpf": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():
            cpf = CPF()

            if cpf.validate(data):
                return True

            session["error_validate"]['cpf'] = "The CPF entered is invalid. Please check the number you entered and try again."
            return False

        session["error_validate"]['cpf'] = "CPF already registered in our systems!"
        return False

    def validate_phone(self, data, region="BR"):
        """
        Valida o número de telefone fornecido. Verifica se o número é válido e se já está registrado no banco de dados.

        Parâmetros:
            data (str): O número de telefone a ser validado.
            region (str): O código do país/região para a validação. O padrão é "BR".

        Retorna:
            bool: Retorna True se o número for válido e não registrado, caso contrário False.
        """
        self.select.exe_select("SELECT phone FROM user_data WHERE phone = %s LIMIT %s", f'{{"phone": "{data}", "LIMIT": "1"}}')

        if not self.select.get_result():
            try:
                # Valida o número de telefone utilizando a biblioteca phonenumbers
                parsed_number = phonenumbers.parse(data, region)

                if phonenumbers.is_valid_number(parsed_number):
                    return True

                session["error_validate"]['phone'] = "The telephone number provided is invalid. Please check the format and try again."
                return False
            except phonenumbers.NumberParseException as e:
                session["error_validate"]['phone'] = "The telephone number provided is invalid. Please check the format and try again."
                print(f"NumberParseException: {e}")  # Para depuração

                return False

        session["error_validate"]['phone'] = "Phone number already registered in our systems."
        return False

    def validate_password(self, data):
        """
        Valida a senha fornecida de acordo com um conjunto de regras definidas.

        Parâmetros:
            data (str): A senha a ser validada.

        Retorna:
            bool: Retorna True se a senha for válida, caso contrário False.
        """
        schema = PasswordValidator()

        schema \
            .min(8) \
            .max(100) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits() \
            .has().no().spaces() \
            .has().symbols()

        if schema.validate(data):
            return True

        session["error_validate"]["password"] = "Invalid password! Follow the password rules below."
        return False

    def encryption(self, user_password, db_password=None):
        """
        Criptografa a senha fornecida ou verifica se a senha fornecida corresponde à senha armazenada no banco de dados.

        Parâmetros:
            user_password (str): A senha do usuário a ser criptografada ou verificada.
            db_password (str, opcional): A senha armazenada no banco de dados para comparação.

        Retorna:
            str: Retorna a senha criptografada se estiver criando uma nova, ou True se as senhas coincidirem.
        """
        if db_password is not None:
            # Verifica se a senha fornecida corresponde à senha no banco de dados
            if "_" in db_password:
                hashed_db = db_password.replace('_', '/')
            else:
                hashed_db = db_password

            if bcrypt.checkpw(user_password.encode("utf-8"), hashed_db.encode('utf-8')):
                return True

            session["error_validate"] = "The password don't match!"
            return False

        # Criptografa a senha fornecida
        password_hashed = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        return password_hashed.decode('utf-8').replace('/', '_')
