from flask import session
from flask_socketio import SocketIO # type: ignore

from .controller.private_pages.Notifications import notifications_bp, NotificationNamespace

socketio = SocketIO()

def init_socketio(app):
    socketio.init_app(app)

def blueprint_notification(app):
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    socketio.on_namespace(NotificationNamespace('/notifications'))
