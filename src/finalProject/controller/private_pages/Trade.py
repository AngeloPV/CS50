from ...renderer import template_render
from ...models.Trade_actions import Trade_actions
from ...controller.public_pages.Error import Error
from ..protected_pages.Coin_conversion import Coin_conversion


from flask import Blueprint, session, request
from flask_socketio import Namespace, emit # type: ignore
from flask.views import MethodView
import json
from datetime import datetime

class Trade(MethodView):
    def __init__(self):
        self.trades = Trade_actions()
        self.get_error = Error()

    def get(self):  
        if 'user_id' in session:
            get_trades = self.trades.get_trades()

            return template_render("trade.html", data=get_trades)

        return self.get_error.show_error("precisa estar logado", 500)
   

trades_bp = Blueprint('trade', __name__)

# Adicionando a rota da classe à blueprint
trades_bp.add_url_rule('/', view_func=Trade.as_view('trade'))

class TradeNamespace(Namespace):
    def on_connect(self):
        emit('response', {'data': 'Connected to trade namespace!'})


    def on_your_trade(self, cond):
        get_trade = Trade_actions().get_trades(cond)

        emit('your_trade', {'data': json.dumps(get_trade, default=self.custom_serializer)}, broadcast=True)
        

    def on_search_trade(self, data, trade_type):
        if data['search_sender'] == 'Select':
            camp_error = '*You need to choose the cryptocurrency!'
            camp_id = 'search_error'
            emit('search_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
            return     
        
        if data['amount_min'] != '' and data['amount_max'] != '':
            if float(data['amount_min']) > float(data['amount_max']):
                camp_error = '*The minimum value cannot be greater than the maximum value!'
                camp_id = 'search_error'
                emit('search_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
                return
        else:
            data['amount_min'] = 0
            data['amount_max'] = 2e9 
        
        search_trade = Trade_actions().search_trade(data, trade_type)
        
        if search_trade and search_trade[0] != None:

            emit('search_trade', {'data': json.dumps(search_trade[0]), 'condition': json.dumps(search_trade[1])}, broadcast=True)
            return

        result_none = '*No results for these values!'
        camp_id = 'search_error'
        emit('search_trade', {'response': json.dumps(result_none), 'id': json.dumps(camp_id)}, broadcast=True)
        return
        

    def on_add_trade(self, data, password):
        for chave, valor in data.items():
            if valor == '' or valor == 'Select' or not password:
                camp_error = '*All fields must be filled in'
                camp_id = 'submit'
                emit('add_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
                return        

        if data['cripto_recepient_id'] == data['cripto_sender_id']:
            camp_error = '*The cryptocurrency you want to exchange cannot be the same as the one you want to receive in exchange!'
            camp_id = 'cripto_sender'
            emit('add_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
            return

        if float(data['amount_min']) > float(data['amount_max']):
            camp_error = '*The minimum value cannot be greater than the estimated value!'
            camp_id = 'cripto_receive'
            emit('add_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
            return
        
        data['amount_cripto_sender'] = round(float(data['amount_cripto_sender']) - (float(data['amount_cripto_sender']) * 0.03), 3)
        
        verify_value_send = Trade_actions().value_account(data['cripto_sender_id'], float(data['amount_cripto_sender']))

        if verify_value_send:

            add_trade = Trade_actions().add_trades(data, password)

            if add_trade:
                response = 'Trade added successfully!!'
                emit('add_trade', {'data': json.dumps(response)}, broadcast=True)
                return
            
            camp_error = '*Four-digit password invalid!'
            camp_id = 'submit'
            emit('add_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
            return
            
        camp_error = "*You don't have enough of this cryptocurrency!"
        camp_id = 'cripto_sender'
        emit('add_trade', {'response': json.dumps(camp_error), 'id': json.dumps(camp_id)}, broadcast=True)
        return
        

    def on_estimulated_value(self, coin, amount, back_coin):
        if coin and amount and coin != back_coin:
            if coin == "Bitcoin":
                back_coin = 'Ethereum'
                conversion = Coin_conversion().get_eth(float(amount))
            else: 
                back_coin = 'Bitcoin'
                conversion = Coin_conversion().get_btc(float(amount))

            if conversion: 
                conversion = round(float(conversion) - (float(conversion) * 0.03), 3)
                emit('estimulated_value', {'conversion': json.dumps(conversion), 'back_coin': json.dumps(back_coin)}, broadcast=True)
                return

        response = '*The cryptocurrency you want to exchange cannot be the same as the one you want to receive in exchange!'
        id = 'cripto_sender'
        emit('estimulated_value', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)


    def on_delete_trade(self, data_id):
        if (data_id):
            delete_trade = Trade_actions().delete_trade(data_id)
            
            response = '*The cryptocurrency you want to exchange cannot be the same as the one you want to receive in exchange!'

            emit('delete_trade', {'response': json.dumps(response)}, broadcast=True)

        
    def on_get_trade(self, data_id, type_modal):
        if(data_id):
            get_trade = Trade_actions().get_trades(True, data_id)
            print(get_trade)
            if get_trade[1][0] != None:
                adress = get_trade[1][0]

            if type_modal == 'y_trade-details':
                get_your_trade = Trade_actions().get_values_trade(data_id)
            else:
                get_your_trade = None

            emit('get_trade', {'response': json.dumps(get_trade[0][0], default=self.custom_serializer), 'user_adress': json.dumps(adress), 
                            'trade_id': json.dumps(data_id), 'trades': json.dumps(get_your_trade)}, broadcast=True)
    
    def custom_serializer(self, obj):
        """
        Custom serializer function to handle datetime objects during JSON serialization.

        Parameters:
        obj (object): The object to be serialized.

        Returns:
        str or TypeError: If the object is a datetime instance, it returns a string in the format '%Y-%m-%d %H:%M:%S'.
                          If the object is not a datetime instance, it raises a TypeError with a descriptive message.
        """
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    

    def on_update_trade(self, dic_send, adress):
        if dic_send['amount_sender'] == '':
            response = '*The field needs to be filled in!'
            id = 'sender_view'
            emit('update_trade', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)
            
            return

        if float(dic_send['max_value']) < float(dic_send['amount_sender']):
            response = '*The amount you want to exchange cannot be greater than the max value!'
            id = 'sender_view'
            emit('update_trade', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)
            
            return
        elif float(dic_send['min_value']) > float(dic_send['amount_sender']):
            response = '*The amount you want to exchange cannot be less than the min value!'
            id = 'sender_view'
            emit('update_trade', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)        
            return
        del dic_send['max_value']
        del dic_send['min_value']
        
        dic_send['amount_sender'] = round(float(dic_send['amount_sender']) - (float(dic_send['amount_sender']) * 0.03), 3)
        dic_send['amount_recipient'] = round(float(dic_send['amount_recipient']) - (float(dic_send['amount_recipient']) * 0.03), 3)

        verify_value_send = Trade_actions().value_account(dic_send['cripto_sender_id'], float(dic_send['amount_sender']))

        if verify_value_send: 
            new_trade = Trade_actions().new_trade(dic_send, adress)

            if new_trade:
                response = 'certo'
                emit('update_trade', {'response': json.dumps(response)}, broadcast=True)
                return

            response = '*Unexpected error contact us if the error persists!'
            id = 'sender_view'
            emit('update_trade', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)
            return 

        response = '*You do not have enough value of this cryptocurrency!'
        id = 'sender_view'
        emit('update_trade', {'response': json.dumps(response), 'id': json.dumps(id)}, broadcast=True)
