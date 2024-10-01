from flask import Flask, session, send_from_directory, g
from .routes import main_routes
#from .controller.protected_pages.translate import Translate
#from .controller.private_pages.Notifications import notifications_bp, NotificationNamespace
#from .socketio_setup import init_socketio, socketio

# from .controller.private_pages.Notifications import Notifications  # Blueprint de notificações
from .config import Config

app = Flask(__name__)

app.register_blueprint(main_routes)  # Registra o blueprint ou as rotas

@app.route('/static/images/dashboard/<path:filename>')
def serve_file(filename):
    return send_from_directory('static/images/dashboard', filename)


config = Config()
config.init_app(app)

#app.register_blueprint(notifications_bp, url_prefix='/notifications')
#socketio.on_namespace(NotificationNamespace('/notifications'))

"""@app.template_filter('translate')
def translate_filter(text, target_language='en'):
    return Translate.translate_text(text, target_language)"""

if __name__ == '__main__':
    app.run(app)
