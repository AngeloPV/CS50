from .db_connection import Conn  # Importando a classe Conn do arquivo db_connection.py
from ..helper.helper_select import Select
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update
from ..helper.helper_insert import Insert
from datetime import datetime
from decimal import Decimal
class User:
    """
    Classe responsavel por manipular os dados do usuario
    """
    def __init__(self):
        self.connection = Conn().connect()  #instacia a classe responsavel pela conexão e inicia a conexão com o banco
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.delete = Delete() #cria uma instancia responsavel pra deletar dados do banco
        self.update = Update() #cria uma instancia responsavel pra atualizar dados do banco
        self.insert = Insert() #cria uma instancia responsavel pra inserir dados no banco
        self.result = None #armazena o resultado

    def set_4_digits_pass(self, password, user_id):
        """
        Define a senha de 4 digitos do usuario

        Parâmetros:
        - password (str): A senha de 4 dígitos a ser definida.
        - user_id (int): O identificador único do usuário.
        """
        
        self.update.exe_update(data={"pass_4_digit": password}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = False)
        return True

    def get_4_digits_pass(self, user_id):
        """
        Recupera a senha de 4 digitos do usuario

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: A senha de 4 dígitos do usuário, ou False caso não exista.
        """
        self.select.exe_select("SELECT pass_4_digit FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        password = self.select.get_result()     
        if not password:
            return False
        return password[0]
        
    
    def set_profile_image(self, img, user_id):
        """
        Define a imagem de perfil do usuário.

        Parâmetros:
        - img (str): Nome da imagem de perfil a ser atribuída ao usuário.
        - user_id (int): O identificador único do usuário.
        """
        self.update.exe_update(data={"img_name": img}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = False)
        
        return True
    
    def get_profile_image(self, user_id):
        """
        Recupera o nome da imagem de perfil do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: Nome da imagem de perfil.
        """
        self.select.exe_select("SELECT img_name FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        img = self.select.get_result()     
        return img[0]
    
    def get_user_name(self, user_id):
        """
        Recupera o nome completo do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - list: Lista contendo os nomes do usuário (primeiro nome, sobrenome).
        """
        self.select.exe_select("SELECT name FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        nome_completo = self.select.get_result() 
        nomes = nome_completo[0].split()    
        return nomes
    
    def get_user_email(self, user_id):
        """
        Recupera o e-mail do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: O e-mail do usuário.
        """
        self.select.exe_select("SELECT email FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        email = self.select.get_result() 
        return email[0]
    
    def get_user_phone(self, user_id):
        """
        Recupera o número de telefone do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: O número de telefone do usuário.
        """
        self.select.exe_select("SELECT phone FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        phone = self.select.get_result() 
        return phone[0]
    
    def get_theme(self, user_id):
        """
        Recupera o tema de interface do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: O tema do usuário (ex.: "light", "dark").
        """
        self.select.exe_select("SELECT theme FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        theme = self.select.get_result() 
        return theme[0]
    
    def set_theme(self, user_id, theme):
        """
        Define o tema de interface do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.
        - theme (str): O novo tema a ser atribuído (ex.: "light", "dark").
        """
        self.update.exe_update(data={"theme": theme}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = False)
        return True
    
    def get_language(self, user_id):
        """
        Recupera o idioma preferido do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: O idioma do usuário (ex.: "pt", "en").
        """
        self.select.exe_select("SELECT language FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        language = self.select.get_result() 
        return language[0]
    
    def delete_account(self, user_id):
        """
        Desativa a conta do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - bool: Resultado da operação de exclusão.
        """
        self.update.exe_update(data={"status": '0'}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = False)
        
        return True
    
    def get_postal_code(self, user_id):
        """
        Recupera o código postal do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - str: O código postal do usuário.
        """
        self.select.exe_select("SELECT cep FROM user_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{user_id}", "LIMIT": 1}}', False)
        postal_code = self.select.get_result() 
        return postal_code[0]
    
    def set_postal_code(self, user_id, postal_code):
        """
        Define o código postal do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.
        - postal_code (str): O novo código postal a ser atribuído ao usuário.
        """
        self.update.exe_update(data={"cep": postal_code}, table_name="user_data", data_where={"id": user_id}, 
                            operator=" =, ="  ,close_conn = False)
        return True
    
    def get_wallet(self, user_id):
        """
        Recupera a carteira do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - dict|False: Dicionário com dados da carteira ou False caso não haja carteira.
        """
        self.select.exe_select(f'SELECT *  FROM wallets WHERE user_id = %s',  
                               f'{{"user_id": "{user_id}"}}', False)
        wallet = self.select.get_result()
        if wallet:
            return wallet[0]
        return False
    
    def update_cash(self, sit, user_id, cash):
        """
        Atualiza o saldo de dinheiro do usuário, com base na situação (ganho ou perda).

        Parâmetros:
        - sit (str): '+' para ganho ou '-' para perda.
        - user_id (int): O identificador único do usuário.
        - cash (float): Valor a ser atualizado no saldo.
        """
        cursor = self.connection.cursor()
        
        if sit == '+':
            query = """INSERT INTO user_cash
                    VALUES ('',%s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE 
                    cash = cash + %s,
                    modified = NOW();"""
        else:
            query = """INSERT INTO user_cash
                    VALUES ('',%s, %s, NOW(), NOW())
                    ON DUPLICATE KEY UPDATE 
                    cash = cash - %s,
                    modified = NOW();"""
            
        cursor.execute(query, (user_id, cash, cash))
        self.connection.commit()
        cursor.close()
        return True
    
    def get_cash(self, user_id):
        """
        Recupera o saldo de dinheiro atual do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - float: O saldo de dinheiro do usuário.
        """
        self.select.exe_select("SELECT cash FROM user_cash WHERE user_id = %s LIMIT %s", 
                               f'{{"user_id": "{user_id}", "LIMIT": 1}}', False)
        cash = self.select.get_result() 
        if not cash:
            return 0
        return cash[0]
    
    def buy_crypto(self, user_id, crypto_id, amount, cost):
        """
        Realiza a compra de uma criptomoeda para o usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.
        - crypto_id (int): O identificador único da criptomoeda.
        - amount (float): A quantidade comprada da criptomoeda.
        - cost (float): O custo total da compra.

        Retorno:
        - bool: Resultado da operação de compra.
        """
        cursor = self.connection.cursor()

        if crypto_id == 'bitcoin':
            crypto_id = 1
            query = """INSERT INTO user_btc
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount + %s,
                modified = NOW();""" 

        elif crypto_id == 'ethereum':
            crypto_id = 2 
            query = """INSERT INTO user_eth
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount + %s,
                modified = NOW();""" 

        cursor.execute(query, (user_id, amount, amount))
        self.connection.commit()
        cursor.close()

        now = datetime.now()

        data = {
            "id": '',
            "user_id": user_id,
            "criptocurrencies_id": crypto_id,
            "amount": amount,
            "cost": cost,
            "created": now
        }
        self.insert.exe_insert(table_name='buy', data=data)
        
        return True

    def sell_crypto(self, user_id, crypto_id, amount, value):
        """
        Realiza a venda de uma criptomoeda para o usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.
        - crypto_id (int): O identificador único da criptomoeda.
        - amount (float): A quantidade vendida da criptomoeda.
        - value (float): O valor total da venda.

        Retorno:
        - bool: Resultado da operação de venda.
        """
        cursor = self.connection.cursor()

        if crypto_id == 'bitcoin':
            crypto_id = 1
            query = """INSERT INTO user_btc
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount - %s,
                modified = NOW();""" 

        elif crypto_id == 'ethereum':
            crypto_id = 2 
            query = """INSERT INTO user_eth
                VALUES ('',%s, %s, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                amount = amount - %s,
                modified = NOW();""" 

        cursor.execute(query, (user_id, amount, amount))
        self.connection.commit()
        cursor.close()

        data = {
            'id': '',
            'user_id': user_id,
            'criptocurrencies_id': crypto_id,
            'amount': amount,
            'created': datetime.now(),
            'value': value
        }
       
        self.insert.exe_insert(table_name='sell', data=data)
        return True

    def get_bitcoin_balance(self, user_id):
        """
        Recupera o saldo de bitcoin atual do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - float: O saldo de bitcoin do usuário.
        """
        self.select.exe_select("SELECT amount FROM user_btc WHERE user_id = %s LIMIT %s", 
                               f'{{"user_id": "{user_id}", "LIMIT": 1}}', False)
        cash = self.select.get_result() 
        if not cash:
            return 0
        return cash[0]
    
    def get_ethereum_balance(self, user_id):
        """
        Recupera o saldo de ethereum atual do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - float: O saldo de ethereum do usuário.
        """
        self.select.exe_select("SELECT amount FROM user_eth WHERE user_id = %s LIMIT %s", 
                               f'{{"user_id": "{user_id}", "LIMIT": 1}}', False)
        cash = self.select.get_result() 
        if not cash:
            return 0
        return cash[0]
    
    def get_buy_data(self, user_id):
        """
        Recupera os dados de compra do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - list: Uma lista de dicionários contendo os dados de compra do usuário.
        """
        # Define os nomes das colunas para a tabela "buy"
        column_names = ['id', 'user_id', 'criptocurrencies_id', 'amount', 'cost', 'created']
        
        # Executa a consulta
        self.select.exe_select("SELECT * FROM buy WHERE user_id = %s", 
                            f'{{"user_id": "{user_id}"}}', False)
        
        # Converte os resultados para uma lista de dicionários
        buy_data = []
        for row in self.select.get_result():
            row_dict = dict(zip(column_names, row))
            
            # Converte o valor de 'amount' para Decimal
            amount_value = Decimal(str(row_dict['amount']))  # Converte para Decimal com precisão exata
            
            # Formata o número para exibir exatamente como no banco de dados (preservando casas decimais)
            row_dict['amount'] = amount_value
            
            buy_data.append(row_dict)
        
        return buy_data

    def get_sell_data(self, user_id):
        """
        Recupera os dados de venda do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - list: Uma lista de dicionários contendo os dados de venda do usuário.
        """
        # Define os nomes das colunas para a tabela "sell"
        column_names = ['id', 'user_id', 'criptocurrencies_id', 'amount', 'created',  'value']
        
        # Executa a consulta
        self.select.exe_select("SELECT * FROM sell WHERE user_id = %s", 
                            f'{{"user_id": "{user_id}"}}', False)
        
        # Converte os resultados para uma lista de dicionários
        sell_data = []
        for row in self.select.get_result():
            row_dict = dict(zip(column_names, row))
            
            # Converte o valor de 'amount' para Decimal
            amount_value = Decimal(str(row_dict['amount']))  # Converte para Decimal com precisão exata
            
            # Formata o número para exibir exatamente como no banco de dados (preservando casas decimais)
            row_dict['amount'] = amount_value
            
            sell_data.append(row_dict)
        
        return sell_data

    def get_trade_data(self, user_id):
        """
        Recupera os dados de trocas do usuário.

        Parâmetros:
        - user_id (int): O identificador único do usuário.

        Retorno:
        - list: Uma lista de dicionários contendo os dados de trocas do usuário.
        """
        # Define os nomes das colunas para a tabela "trades"
        column_names = [
            'id', 'cripto_sender_id', 'cripto_recipient_id', 'user_sender_id', 
            'user_recipient_id', 'reg_trade_id', 'amount_sender', 
            'amount_recipient', 'created', 'modified', 'rate'
        ]
        
        # Executa a consulta
        self.select.exe_select("SELECT * FROM trades WHERE user_sender_id = %s OR user_recipient_id = %s", 
                            f'{{"user_sender_id": "{user_id}", "user_recipient_id": "{user_id}"}}', False)
        
        # Converte os resultados para uma lista de dicionários
        trade_data = [dict(zip(column_names, row)) for row in self.select.get_result()]
        return trade_data
