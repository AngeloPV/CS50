from flask import Flask, send_from_directory, session, g
from .routes import main_routes
from .socketio_setup import init_socketio, blueprint_notification, socketio
import os
from .context_processor import notifications_processor  


# from .controller.private_pages.Notifications import Notifications  # Blueprint de notificações
from .config import Config

app = Flask(__name__)


@app.context_processor # defines a global variable for all templates
def processor_add_notifications_processor():
    return notifications_processor()  


app.register_blueprint(main_routes)  # Register the blueprint 

@app.route('/static/images/dashboard/<path:filename>')
def serve_file(filename):
    return send_from_directory('static/images/dashboard', filename)

# Adicione a rota do favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images', 'sidebar'), 
                               'logo.png', 
                               mimetype='image/png')


# socketio = SocketIO(app)
init_socketio(app)
blueprint_notification(app)

config = Config()
config.init_app(app)


#import logging9
#ilogging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    socketio.run(app)
