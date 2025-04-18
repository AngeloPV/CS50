from flask import session
from flask_socketio import SocketIO # type: ignore

from .controller.private_pages.Notifications import notifications_bp, NotificationNamespace
from .controller.private_pages.Trade import trades_bp, TradeNamespace
# socketio = SocketIO(cors_allowed_origins="*", logger=True, engineio_logger=True)
socketio = SocketIO(cors_allowed_origins="*")

def init_socketio(app):
    socketio.init_app(app)

def blueprint_notification(app):
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    socketio.on_namespace(NotificationNamespace('/notifications'))

def blueprint_trade(app):
    app.register_blueprint(trades_bp, url_prefix='/trade')
    socketio.on_namespace(TradeNamespace('/trade'))
