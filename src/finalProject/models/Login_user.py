from flask import url_for

from ..helper.helper_select import Select
from ..helper.valitade import Validate

from flask import session

class Login_user():
    """
    Classe responsável pelo processo de login do usuário, incluindo verificação de credenciais,
    validação de e-mail e criação de sessão.
    """
    def __init__(self):
        
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.validate = Validate() #cria uma instancia responsavel pela validação

        self.data = None  # Armazena os dados do usuário recebidos durante o login
        self.result = None # Armazena o resultado da consulta ao banco de dados

    def verify_login(self, data):
        """
        Verifica as credenciais de login fornecidas pelo usuário.

        Parâmetros:
        - data (dict): Dicionário contendo os dados do usuário, como nome, e-mail, CPF e senha.

        Retorno:
        - bool: Retorna True se as credenciais forem válidas e o login for bem-sucedido, False caso contrário.
        """
        self.data = data

        self.select.exe_select("SELECT id, name, password, status FROM user_data WHERE email = %s OR cpf = %s OR name = %s LIMIT %s", 
                               f'{{"email": "{self.data["user"]}", "cpf": "{self.data["user"]}", "name": "{self.data["user"]}", "LIMIT": 1}}', False)
        self.result = self.select.get_result()
        
        if self.result:
            # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
            if self.validate.encryption(data['password'], self.result[2]):
                # Verifica se o e-mail foi confirmado
                if self.verify_email_sit():
                    session['user_id'] = self.result[0] # Armazena o ID do usuário na sessão
                    print(session['user_id'])
                    return True #retorna true se o login for bem-sucedido
                
                # Se o e-mail não foi confirmado, retorna uma mensagem de erro e um link para reenvio de confirmação
                link = url_for("main_routes.route_method", route_name="Resend_authentication_email", method="index")
                session["error_message"] = f'You need to confirm your email, request a new link: <a href="{link}" class="link" style="color: #1B263B">Confirm Email</a>'
                return False
            
            # Se a senha fornecida for inválida, retorna uma mensagem de erro
            session["error_message"] = "Invalid username or password field"
            return False
        
        # Se o usuário não for encontrado, retorna uma mensagem de erro
        session["error_message"] = "Invalid username or password field"
        return False


    def verify_email_sit(self):
        """
        Verifica se o e-mail do usuário foi confirmado.

        Retorno:
        - bool: Retorna True se o e-mail foi confirmado, False caso contrario.
        """
        self.select.exe_select("SELECT email_sit FROM email_sit WHERE email_id = %s AND user_id = %s LIMIT %s", 
                        f'{{"email_id": "2", "user_id": "{self.result[0]}", "LIMIT": 1 }}', True)
        result_email_sit = self.select.get_result()

        if result_email_sit:
            if result_email_sit[0] == 0:
                return True
            
            return False
        
        return False

    def verify_user_sit(self):
        """
        Antes de efetivar o login, verifica se a conta do usuário já foi desativa, se ja tiver sido desativada
        não permite que o usuario entre novamente, a verificação é feita com base na coluna status da tabela user_data
        se for 1 o usuário esta liberado para usar o sistema, se for 0 o usuário consta como desativado

        Retorno:
        - bool: Retorna True se a conta do usuário estiver ativa, False caso contrario
        """

        if self.result[3] == 1:
            return True
        return False