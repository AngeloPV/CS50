from flask import request, session
from datetime import datetime

from ..helper.helper_select import Select
from ..helper.helper_update import Update
from ..helper.valitade import Validate
from ..helper.send_email import Send_Email


class Update_password:
    """
    Classe responsável por gerenciar o processo de mudança de senha do usuario
    """
    def __init__(self):
        self.select = Select()
        self.validate = Validate() #cria uma instancia responsavel pela validação
        self.update = Update() #cria uma instancia responsavel pra atualizar dados do banco


    def new_password(self, password):
        """
        Verifica se o e-mail fornecido é válido e se a situação de confirmação do e-mail já foi processada.
        Se necessário, envia um novo e-mail de autenticação.

        Parâmetros:
        - email (dict): Dicionário contendo o endereço de e-mail a ser verificado.

        Retorno:
        - bool: Retorna True se o e-mail foi verificado e o processo de reenvio foi bem-sucedido, 
                ou False caso contrário.
        """
        self.select.exe_select("SELECT id, password FROM user_data WHERE email = %s LIMIT %s", f'{{"email": "{session["user_email"]}", "LIMIT": "1"}}', True)

        #valida a senha
        if self.validate.validate_password(password):
            if self.validate.encryption(password, self.select.get_result()[1]):
                session["error_validate"]['password'] = "New password cannot be the same as the previous one!"
                return False
            if self.update_password(self.validate.encryption(password), self.select.get_result()[0]):
                return True
            return False
      
        return False

    def update_password(self, password, id):

        data = {'password': password}
        print(password)
        data_where = {'id': id}

        self.update.exe_update(data=data, table_name="user_data", data_where=data_where, operator=' =, =', close_conn=True)

        if self.update.getResult():
            return True
        
        return False