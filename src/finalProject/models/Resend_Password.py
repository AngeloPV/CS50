from flask import session
from datetime import datetime

from ..helper.helper_select import Select
from ..helper.valitade import Validate
from ..helper.send_email import Send_Email
from ..controller.protected_pages.Type_email import Type_email


class Resend_Password:
    """
    Classe responsável por gerenciar o processo de enviar o e-mail de recuperar senha de  usuário.
    Ela lida com a verificação do e-mail e o envio do e-mail com um código de autenticação.
    """
    def __init__(self):
        self.select_send = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.validate = Validate() #cria uma instancia responsavel pela validação
        self.send_email = Send_Email() #cria uma instancia responsavel pra enviar emails
        self.type = Type_email() #cria uma instancia responsaevel por determinar o provedor do email

        self.data_email = None  #Variável para armazenar os dados do e-mail
        self.user_authentication_id = None  # Variável para armazenar o ID de autenticação do usuário

    def verify_email_recover(self, email):
        """
        Verifica se o e-mail fornecido é válido e se a situação de confirmação do e-mail já foi processada.
        Se necessário, envia um novo e-mail de autenticação.

        Parâmetros:
        - email (dict): Dicionário contendo o endereço de e-mail a ser verificado.

        Retorno:
        - bool: Retorna True se o e-mail foi verificado e o processo de reenvio foi bem-sucedido, 
                ou False caso contrário.
        """
        self.data_email = email
        self.select_send.exe_select("SELECT id, name, email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{self.data_email["email"]}", "LIMIT": "1"}}', True)

        #valida o email
        if self.validate.validate_email(self.data_email['email'], False):
            if self.email_resend(): # Envia o e-mail de autenticação novamente
                return True
            return False
      
        return False
    
    def email_resend(self):
        """
        Envia um e-mail de recuperar senha para o endereço de e-mail fornecido.

        Retorno:
        - bool: Retorna True se o e-mail foi enviado com sucesso, ou False caso contrário.
        """
        email_data = self.select_send.get_result()

        if email_data:
            # Formata os dados do e-mail para enviar na mensagem

            email_data = {"id": email_data[0], "name": email_data[1], "verify": datetime.date, "email": email_data[2]}
            
            # Url para o link de autenticação
            url = "Recover_Password/index/"
            
            # Determina o provedor do e-mail para configurar o envio corretamente
            self.type.get_type(email_data['email'])
            
            if self.send_email.config_email(3, email_data, url, 'code', 'Recover Password'):
                #pega o código gerado e armazena na sessao
                session['code'] = self.send_email.get_code()

                session["user_authentication_id"] = email_data["id"]
                session['type_email'] = 3

                return True

            return False
        
        session["error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False

