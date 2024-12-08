from flask import session

from ..helper.helper_update import Update
from ..helper.helper_select import Select
from ..helper.valitade import Validate


class Authenticate_account_user:
    """
    Classe responsavel por gerenciar a autenticação e atualização de informações
    relacionadas à conta do usuário para saber se o usuário está verificado
    """
    def __init__(self):
        self.update_sit = Update() #cria uma instancia responsavel pra atualizar dados do banco
        self.select_user = Select()  #cria uma instancia responsavel pra resgatar dados do banco
        self.validate = Validate() #cria uma instancia responsavel pela validação
        self.user_data = None #variavel que recebe os dados do usuario
        self.user_authentication_id = None #variavel que recebe o id do usuario

    def update_account(self, id_user):
        """
        Atualiza a conta do usuario chamando a função update_sit_account, retorna boolean
        """
        self.user_authentication_id = id_user

        if self.update_sit_account():
            return True
            
        return False
        

    def update_sit_account(self):
        """
        Atualiza a situação do email associado ao usuario
        """
        #dados para a query
        data = {'email_sit': 0}
        data_where = {'email_id': session['type_email'], 'user_id': self.user_authentication_id}
        
        #query
        self.update_sit.exe_update(data=data, table_name="email_sit", data_where=data_where, operator=' =, =, =', close_conn=False)
        
        #se a query for bem sucedida, atualiza a confirmação de email, caso não retorna false
        if self.update_sit.getResult():
            if self.update_conf_email():
                return True
            
            print('Error conf_email')
            return False
        
        return False
    
        
    def update_conf_email(self):
        """
        Remove a confirmação de email da conta do usuario, retorna o resultado da query update
        """
        #dados para a query
        data = {'conf_email': None}
        data_where = {'id': self.user_authentication_id}
        
        #query
        self.update_sit.exe_update(data=data, table_name="user_data", data_where=data_where, operator=' =, =', close_conn=True)
        
        return self.update_sit.getResult()
