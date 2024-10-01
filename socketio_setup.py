from flask_socketio import SocketIO # type: ignore

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app)
