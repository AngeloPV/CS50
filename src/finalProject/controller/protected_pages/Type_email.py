import re
from flask import session 
from ...app import app
from ...config import Config


class Type_email:
    """
    Classe responsável por determinar o provedor de e-mail do usuário
    com base no domínio do e-mail fornecido, e atualizar as configurações 
    associadas ao provedor.
    """
    def __init__(self): 
        self.email_config = Config() #Instância da classe 'Config' para acessar as configurações de e-mail
        self.result = None # Resultado que armazenará o provedor de e-mail encontrado
        self.current_provider = 'gmail'  # Provê o provedor de e-mail inicial (gmail)

    def get_result_email(self):
        """
        Retorna o provedor de e-mail encontrado.
        """
        return self.result
    
    def get_type(self, email):
        """
        Extrai o provedor de e-mail do endereço de e-mail fornecido e atualiza as configurações
        associadas a esse provedor, se necessário.

        Parâmetros:
        - email (str): O endereço de e-mail a ser analisado.

        Retorno:
        - bool: Retorna True se o provedor de e-mail foi identificado e a configuração foi atualizada (se necessário),
                ou None caso o endereço de e-mail não contenha um provedor válido.
        """
        # Utiliza expressão regular para extrair o provedor do e-mail

        match = re.search(r'@(.+?)\.', email)

        if match:
            provider = match.group(1)  # Pega o provedor encontrado
            
            # Verifica se o provedor mudou em relação ao provedor atual

            if provider != self.current_provider: 
                self.current_provider = provider  
                # Atualiza as configurações do provedor de e-mail
                with app.app_context():
                    self.email_config.get_set_email(app, self.current_provider)  # Update settings

            self.result = provider # Armazena o provedor encontrado
            return True # Retorna True se o provedor foi identificado

        return None # Retorna None se o endereço de e-mail nao contiver um provedor valido
