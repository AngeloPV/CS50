from flask import Flask
from .routes import main_routes
from .controller.private_pages.Notifications import notifications_bp, NotificationNamespace
from .socketio_setup import init_socketio, socketio

# from .controller.private_pages.Notifications import Notifications  # Blueprint de notificações
from .config import Config

app = Flask(__name__)

app.register_blueprint(main_routes)  # Registra o blueprint ou as rotas

# socketio = SocketIO(app)
init_socketio(app)


config = Config()
config.init_app(app)

app.register_blueprint(notifications_bp, url_prefix='/notifications')
socketio.on_namespace(NotificationNamespace('/notifications'))


if __name__ == '__main__':
    socketio.run(app)
