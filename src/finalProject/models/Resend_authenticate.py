from flask import request, redirect, url_for, session
from datetime import datetime

from ..helper.helper_select import Select
from ..helper.helper_update import Update
from ..helper.valitade import Validate
from ..helper.send_email import Send_Email
from ..controller.protected_pages.Type_email import Type_email


class Resend_authenticate:
    """
    Classe responsável por gerenciar o processo de reenvio do e-mail de autenticação para o usuário.
    Ela lida com a verificação do e-mail, o envio do e-mail com um código de autenticação e a atualização da 
    situação de confirmação do e-mail no banco de dados.
    """
    def __init__(self):
        self.select_send = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.validate = Validate() #cria uma instancia responsavel pela validação
        self.send_email = Send_Email() #cria uma instancia responsavel pra enviar emails
        self.update_sit = Update() #cria uma instancia responsavel pra atualizar dados do banco
        self.type = Type_email() #cria uma instancia responsaevel por determinar o provedor do email

        self.data_email = None  #Variável para armazenar os dados do e-mail
        self.user_authentication_id = None  # Variável para armazenar o ID de autenticação do usuário

    def verify_email(self, email):
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
        self.select_send.exe_select("SELECT id, name, email, conf_email FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{self.data_email["email"]}", "LIMIT": "1"}}', True)

        #valida o email
        if self.validate.validate_email(self.data_email['email'], False):
            # Verifica e atualiza a situação de confirmação do e-mail
            if self.update_conf_email():
                if self.email_resend(): # Envia o e-mail de autenticação novament
                    return True
                return False
            return False
      
        return False
    
    def email_resend(self):
        """
        Envia um e-mail de autenticação para o endereço de e-mail fornecido.

        Retorno:
        - bool: Retorna True se o e-mail foi enviado com sucesso, ou False caso contrário.
        """
        email_data = self.select_send.get_result()

        if email_data:
            # Formata os dados do e-mail para enviar na mensagem

            email_data = {"id": email_data[0], "name": email_data[1], "verify": email_data[3], "email": email_data[2]}
            
            # Url para o link de autenticação
            url = "Authenticate_account/index/"
            
            # Determina o provedor do e-mail para configurar o envio corretamente
            self.type.get_type(email_data['email'])
            
            if self.send_email.config_email(2, email_data, url, 'code', 'Autenticar Email'):
                #pega o código gerado e armazena na sessao
                session['code'] = self.send_email.get_code()

                session["user_authentication_id"] = email_data["id"]
                session['type_email'] = 2

                return True

            return False
        
        session["error_send_email"] = "Não foi possivel realizar o select para pegar os dados do email"
        return False


    def update_conf_email(self):
        """
        Atualiza a situação de confirmação do e-mail para o usuário, se necessário.
        Verifica se o e-mail ainda não foi confirmado e, caso afirmativo, atualiza o campo 'conf_email' 
        com a data atual.

        Retorno:
        - bool: Retorna True se a atualização foi bem-sucedida ou se o e-mail já está confirmado, 
                ou False caso contrário.
        """
        if self.select_send.get_result()[3] == None:
            # encriptografa a data atual
            data = {'conf_email': self.validate.encryption(str(datetime.now().date()))}
            # Obtém o ID do usuário para atualização
            data_where = {'id': self.select_send.get_result()[0]}
            
            # Atualiza o campo 'conf_email' na tabela 'user_data'
            self.update_sit.exe_update(data=data, table_name="user_data", data_where=data_where, operator=' =, =', close_conn=True)
            
            # Retorna o resultado da atualização
            return self.update_sit.getResult()
        return True