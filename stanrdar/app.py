from flask import Flask, send_from_directory, g
from .routes import main_routes
from .socketio_setup import init_socketio, blueprint_notification, socketio

# from .controller.private_pages.Notifications import Notifications  # Blueprint de notificações
from .config import Config

app = Flask(__name__)

app.register_blueprint(main_routes)  # Registra o blueprint ou as rotas

@app.route('/static/images/dashboard/<path:filename>')
def serve_file(filename):
    return send_from_directory('static/images/dashboard', filename)

# socketio = SocketIO(app)
init_socketio(app)
blueprint_notification(app)

config = Config()
config.init_app(app)


if __name__ == '__main__':
    socketio.run(app)
