from flask import Blueprint, session
from flask_socketio import Namespace, emit # type: ignore
from flask.views import MethodView
import json
from datetime import datetime


from ...models.Get_notification import Get_notifications
from ...renderer import template_render
from ...controller.public_pages.Error import Error
from ..protected_pages.Count_notifications import Count_notifications


# Classe notifications que será chamada pela URL 
class Notifications(MethodView):
    def __init__(self):
        self.get_error = Error()
        self.get_notification = Get_notifications()


    def get(self, type='standard'):
        if 'user_id' in session:

            session['viewd_count'] = True
            
            if 'type' in session:
                session['type'] = type 

                select_result = self.get_notification.select_notifcation(session['type'])
                if select_result:
                    return select_result

                return None
            else:             
                select_result = self.get_notification.select_notifcation(type)

                if select_result != False:  
                    return template_render("notifications.html", data=select_result[0], type=type, count_notifcations=select_result[1])
                
                return template_render("notifications.html", type=type, count_notifcations=select_result[1])
                
        return self.get_error.show_error("precisa estar logado", 500)

    
# Definindo o blueprint
notifications_bp = Blueprint('notifications', __name__)

# Adicionando a rota da classe à blueprint
notifications_bp.add_url_rule('/', view_func=Notifications.as_view('notifications'))

# Definindo um namespace para as notificações
class NotificationNamespace(Namespace):
    def on_connect(self):
        emit('response', {'data': 'Connected to notifications namespace!'})


    def on_delete(self, data, actual_type):

        if isinstance(data, list) or isinstance(data, int):

            result_delete = Get_notifications().delete_notifications(data)

            if result_delete:
                session['type'] = actual_type

                teste = Notifications()
                select = teste.get(type=session['type'])
                    
                emit('delete', {'data': json.dumps(select[0], default=self.custom_serializer), 'count': json.dumps(select[1])}, broadcast=True)
            else:
                emit('delete', {'data': 'Notificações não deletadas'}, broadcast=True)
 

    def on_verify_type(self, value_update, data, actual_type=None):
        if (isinstance(data, list) or isinstance(data, int)) and value_update is not None:
            result_archive = Get_notifications().update_notifications(value_update, data)
    
            if result_archive:
                session['type'] = actual_type

                teste = Notifications()
                select = teste.get(type=session['type'])
                    
                emit('verify_type', {'data': json.dumps(select[0], default=self.custom_serializer), 'count': json.dumps(select[1])}, broadcast=True)


    def on_change_type(self, type):
        
        session['type'] = type

        teste = Notifications()
        select = teste.get(type=session['type'])

        emit('change_type', {'data': json.dumps(select[0], default=self.custom_serializer), 'count': json.dumps(select[1])}, broadcast=True)
        

    def custom_serializer(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')