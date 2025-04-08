from ..helper.helper_select import Select
from ..helper.helper_insert import Insert
from ..helper.helper_delete import Delete
from ..helper.helper_update import Update
from ..helper.valitade import Validate

from flask import session

class Trade_actions:
    def __init__(self):
        self.select = Select()
        self.insert = Insert()
        self.validate = Validate()
        self.update = Update()
        self.delete_notification = Delete()

        self.result = None

    def get_user_adresses(self, user_id, acronym_sender):
        self.select.exe_select(f'SELECT public_key FROM wallets WHERE user_id = %s AND currency = %s',  
                               f'{{"user_id": "{user_id}", "currency": "{acronym_sender}"}}', False)

        self.result = self.select.get_result()

        if self.result:
            return self.result
        
        return None 
    
    def get_user_id(self, user_adress):
        self.select.exe_select(f'SELECT user_id FROM wallets WHERE public_key = %s',  
                               f'{{"public_key": "{user_adress}"}}', False)

        self.result = self.select.get_result()

        if self.result:
            print(self.result)
            return self.result[0][0]
        
        return None 

    def get_trades(self, cond=False, data_id=None):
        condition = "!="
        if cond == True:
            condition = "="
        
        camp_id = 'user_id'
        select_id = session["user_id"] 

        if data_id is not None:
            camp_id = 'reg_trade.id' 
            select_id = data_id

        self.select.exe_select(f'''SELECT user_id, amount_min, amount_max, sender.acronym, recipient.acronym, sender.cripto_name, 
                                recipient.cripto_name, amount_cripto_sender, reg_trade.id, reg_trade.created FROM reg_trade 
                                INNER JOIN criptocurrencies AS sender ON cripto_sender_id = sender.id 
                                INNER JOIN criptocurrencies AS recipient ON cripto_recepient_id = recipient.id WHERE {camp_id} {condition} %s''', 
                                f'{{"{camp_id}": "{select_id}"}}', False)

        self.result = self.select.get_result()

        if self.result:
            new_result = list(self.select.get_result())
            for i, select in enumerate(new_result):
                select = list(select) 

                teste = self.get_values_trade(select[-1])

                if teste[0][0] != None and teste[0][1] != None:
                    select[2] = round(float(select[2]) - float(teste[0][0]), 3)
                    select[7] = round(float(select[7]) - float(teste[0][1]), 3)

                new_result[i] = select

            if data_id is not None: 
                return new_result, self.get_user_adresses(new_result[0][0], new_result[0][3])
            
            return new_result
        
        return None 

    
    def get_values_trade(self, trade_id):
        self.select.exe_select(f'''SELECT ROUND(SUM(amount_sender), 3), ROUND(SUM(amount_recipient), 3), COUNT(*) FROM 
                               trades WHERE reg_trade_id = %s''',
                               f'{{"reg_trade_id": "{trade_id}"}}', False) 
        
        self.result = self.select.get_result()
        if self.result:
            return self.result
        
        return None


    def search_trade(self, data, trade_type):
        
        condition = "!="
        back_condition = True
        if trade_type == 'own_trades':
            condition = "="
            back_condition = False


        self.select.exe_select(f'''SELECT user_id, amount_min, amount_max, sender.acronym, recipient.acronym, sender.cripto_name, 
                                amount_cripto_sender, reg_trade.id FROM reg_trade 
                                INNER JOIN criptocurrencies AS sender ON cripto_sender_id = sender.id
                                INNER JOIN criptocurrencies AS recipient ON cripto_recepient_id = recipient.id 
                                WHERE sender.cripto_name = %s AND amount_min >= %s AND amount_max <= %s AND user_id {condition} %s''', 
                                f'''{{"cripto_name": "{data['search_sender']}", "amount_min": "{data['amount_min']}", 
                                "amount_max": "{data['amount_max']}", "user_id": "{session["user_id"]}"}}''', False)
                       
        
        self.result = self.select.get_result()

        if self.result:
            return self.result, back_condition
        
        return None
    
    def add_trades(self, data, password):
        self.select.exe_select(f"""SELECT id FROM criptocurrencies WHERE cripto_name = '{data['cripto_sender_id']}' UNION 
                               SELECT id FROM criptocurrencies WHERE cripto_name = '{data['cripto_recepient_id']}'""")
        
        self.result = self.select.get_result() 

        data['cripto_sender_id'] = self.result[0][0]
        data['cripto_recepient_id'] = self.result[1][0]

        if self.verify_password(password):
            if self.result: 
                data['user_id'] = session["user_id"]
                data['trade_sit'] = 1

                self.insert.exe_insert(data, "reg_trade", None, True)
                result = self.insert.getResult()

                if result:
                    return True
                
        return False
        

    def verify_password(self, password):
        self.select.exe_select(f'''SELECT pass_4_digit FROM user_data WHERE id = %s''',
                               f'{{"user_id": "{session["user_id"]}"}}', False) 
        self.result = self.select.get_result()
        
        print(self.result[0][0])
        if self.result:
            if self.validate.encryption(password, self.result[0][0]):
                return True
            
        return False
    

    def delete_trade(self, data_id):
        if isinstance(data_id, list):
            placeholder = ','.join(['%s'] * len(data_id))
            self.delete_notification.exe_delete("reg_trade", data_id, f'id IN ({placeholder})', False)
        elif isinstance(data_id, int):
            self.delete_notification.exe_delete("reg_trade", data_id, f'id = %s', False)

        if self.delete_notification.getResult():
            return True
        
        return False

    def value_account(self, coin, amount_send):
        amount = self.get_amount_coin(session['user_id'], coin)

        if amount != 0:
            if amount_send <= amount:
                return True
            
            return False

        return False
    

    def new_trade(self, dic_send, adress):
        cripto_sender = dic_send['cripto_sender_id']
        cripto_recipient = dic_send['cripto_recipient_id']

        self.select.exe_select(f"""SELECT id FROM criptocurrencies WHERE cripto_name = '{cripto_sender}' UNION SELECT id FROM criptocurrencies WHERE cripto_name = '{cripto_recipient}'""")
        
        self.result = self.select.get_result() 

        dic_send['cripto_sender_id'] = self.result[0][0]
        dic_send['cripto_recipient_id'] = self.result[1][0]

        if self.result:
            dic_send['user_sender_id'] = session['user_id']
            dic_send['user_recipient_id'] = self.get_user_id(adress)

            if dic_send['user_recipient_id'] != None:
                
                self.insert.exe_insert(dic_send, "trades", None, True)
                result = self.insert.getResult()

                if result:
                    self.update_amount_user(dic_send['user_sender_id'], dic_send['amount_recipient'], cripto_recipient, True)
                    self.update_amount_user(dic_send['user_sender_id'], dic_send['amount_sender'], cripto_sender, False)
                    self.update_amount_user(dic_send['user_recipient_id'], dic_send['amount_sender'], cripto_sender, True)    
                    return True
                
        return False
    

    def update_amount_user(self, user_id, amount, coin, cond):
        print(user_id, amount, coin)
        amount_coin = self.get_amount_coin(user_id, coin)

        if cond:
            amount_coin = float(amount_coin) + float(amount)
        else:
            amount_coin = float(amount_coin) - float(amount)

        dic_update = {'amount': amount_coin}
        dic_where = {'user_id': user_id}

        table = 'user_eth'

        if coin == 'Bitcoin':
            table = 'user_btc'

        self.update.exe_update(data=dic_update, table_name=table, data_where=dic_where, operator=' =, =', close_conn=False)

        if self.update.getResult():
            return True
        
        return False
    

    def get_amount_coin(self, user_id, coin):
        table = 'user_eth'

        if coin == 'Bitcoin':
            table = 'user_btc'

        self.select.exe_select(f'''SELECT amount FROM {table} WHERE user_id = %s''',
                            f'{{"user_id": {user_id}}}', False) 
        self.result = self.select.get_result()

        if self.result:
            return self.result[0][0]
        
        return 0
    