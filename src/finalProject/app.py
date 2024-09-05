from flask import Flask
from .routes import main_routes

import os
from .config import Config

app = Flask(__name__)
app.register_blueprint(main_routes)  # Registra o blueprint ou as rotas

config = Config()
config.init_app(app)


if __name__ == "__main__":
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', 5555))
    except ValueError:
        PORT = 5555

    # Supondo que você esteja usando Flask ou algo similar
    app.run(host=HOST, port=PORT)
    # print(f"Running server on {HOST}:{PORT}")

    app.run(debug=True)
