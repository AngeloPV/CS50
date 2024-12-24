from ..helper.helper_insert import Insert
from ..helper.helper_select import Select
from ..helper.send_email import Send_Email
from ..helper.valitade import Validate

from datetime import datetime
from flask import session
import bcrypt # type: ignore

# Fazer o conf_email


class Register_user():
    """
    Classe responsável pelo processo de registro de um novo usuário.
    Inclui a validação de campos, inserção de dados no banco de dados,
    e envio de e-mail de confirmação.
    """ 
    def __init__(self):
        self.insert = Insert() #cria uma instancia responsavel pra inserir dados no banco
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.send_email = Send_Email() #cria uma instancia responsavel pra enviar emails
        self.validate = Validate() #cria uma instancia responsavel pela validação 
        self.data = None # Armazena os dados do usuário fornecidos no registro

    def addUser(self, data):
        """
        Adiciona um novo usuário ao sistema. Realiza a criação da tabela caso não exista,
        valida os campos do formulário, criptografa a senha e o código de confirmação de e-mail,
        e insere os dados do usuário no banco de dados.

        Parâmetros:
        - data (dict): Dicionário contendo as informações do usuário (nome, e-mail, CPF, etc.)

        Retorno:
        - bool: Retorna True se o registro for bem-sucedido e o e-mail de confirmação for enviado, False caso contrário.
        """
        self.data = data
        
        #cria a tabela caso n exista
        create = ("""
            CREATE TABLE IF NOT EXISTS user_data (
                id int(11) PRIMARY KEY NOT NULL,
                name text NOT NULL,
                email varchar(220) NOT NULL,
                cpf varchar(14) NOT NULL,
                phone varchar(13) NOT NULL,
                password text NOT NULL,
                pass_4_digit varchar(4) DEFAULT NULL,
                img_name text DEFAULT NULL,
                conf_email varchar(220) NULL,
                created datetime DEFAULT current_timestamp(),
                modified datetime DEFAULT NULL,
                language varchar(50),
                theme varchar(50),
                cep varchar(9) DEFAULT NULL,
                status TINYINT(1) DEFAULT 1

            )
        """)

        #valida os campos
        if(self.validate_camps()):
            data['password'] = self.validate.encryption(data['password'])

            data['conf_email'] = self.validate.encryption(str(datetime.now().date()))

            #define valores padrão
            data['theme'] = 'light-theme'
            data['language'] = 'english'
            data['status'] = 1

            #formata o nome
            data['name'] = data['name'].title()

            #Insere os dados do novo usuario no banco
            self.insert.exe_insert(self.data, "user_data", create, True)
            result = self.insert.getResult()

            if result:
                if(self.email()):
                    return True
                
                return False
            
            return False
        
        return False


    def validate_camps(self):
        """
        Função responsável pela validação dos campos do formulário de registro de usuário.
        """
        if (self.validate.validate_email(self.data['email'], False) and self.validate.validate_cpf(self.data['cpf']) 
            and self.validate.validate_phone(self.data['phone']) and self.validate.validate_password(self.data['password'])):
            return True
        
        return False


    def email(self):
        """
        Envia o e-mail de confirmação para o usuário.
        """
        self.select.exe_select("SELECT id, name, email, conf_email FROM user_data WHERE cpf = %s LIMIT %s", f'{{"cpf": "{self.data["cpf"]}", "LIMIT": "1"}}', True)
        email_data = self.select.get_result()

        if email_data:
            email_data = {"id": email_data[0], "name": email_data[1], "verify": email_data[3], "email": email_data[2]}
            
            url = "Authenticate_account/index/"

            # set the provider used to send the email
            # self.type.get_type(email_data['email'])

            if(self.send_email.config_email(2, email_data, url, 'code', 'Authenticate Email')):
                #pega o código gerado e armazena na sessao
                session['code'] = self.send_email.get_code()

                session["user_authentication_id"] = email_data["id"]
                session['type_email'] = 2

                return True

            return False
        
        session["error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False