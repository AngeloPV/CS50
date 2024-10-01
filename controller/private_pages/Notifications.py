"""from flask import Blueprint, render_template
from flask_socketio import Namespace, emit # type: ignore
from flask.views import MethodView


# FAZER O CSS DA PAGINA NOTIFICAÇÕES
# LISTAR TODOS AS NOTIFCAÇÕES DO USER
# MARCAR COMO LIDA AS NOTIFCAÇÕES
    # TODAS
    # SELECIONASD
# APAGAR AS NOTIFICAÇÕES
    # TODAS
    # SELECIONASD

# Classe notifications que será chamada pela URL 
class Notifications(MethodView):
    def get(self):
        return render_template("notifications.html")
        # return render_template("notifications.html")
    
# Definindo o blueprint
notifications_bp = Blueprint('notifications', __name__)

# Adicionando a rota da classe à blueprint
notifications_bp.add_url_rule('/', view_func=Notifications.as_view('notifications'))

# Definindo um namespace para as notificações
class NotificationNamespace(Namespace):
    def on_connect(self):
        emit('response', {'data': 'Connected to notifications namespace!'})

    def on_my_event(self, data):
        print('Received data:', data)
        data['message'] = "AMOR DO FELIOPE"
        emit('response', {'data': data['message']}, broadcast=True)
"""