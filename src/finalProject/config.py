from datetime import timedelta
import os
from dotenv import load_dotenv # type: ignore
from flask import session

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    def get_set_email(self, app, provider):
        MAIL_SERVERS = {
            'gmail': {
                'MAIL_SERVER': os.getenv('GMAIL_MAIL_SERVER'),
                'MAIL_PORT': os.getenv('GMAIL_MAIL_PORT'),
                'MAIL_USERNAME': os.getenv('GMAIL_MAIL_USERNAME'),
                'MAIL_PASSWORD': os.getenv('GMAIL_MAIL_PASSWORD'),
                'MAIL_USE_TLS': os.getenv('GMAIL_MAIL_USE_TLS') == 'True',
                'MAIL_USE_SSL': os.getenv('GMAIL_MAIL_USE_SSL') == 'True'
            },
            'yahoo': {
                'MAIL_SERVER': os.getenv('YAHOO_MAIL_SERVER'),
                'MAIL_PORT': os.getenv('YAHOO_MAIL_PORT'),
                'MAIL_USERNAME': os.getenv('YAHOO_MAIL_USERNAME'),
                'MAIL_PASSWORD': os.getenv('YAHOO_MAIL_PASSWORD'),
                'MAIL_USE_TLS': os.getenv('YAHOO_MAIL_USE_TLS') == 'True',
                'MAIL_USE_SSL': os.getenv('YAHOO_MAIL_USE_SSL') == 'True'
            },
            'outlook': {
                'MAIL_SERVER': os.getenv('OUTLOOK_MAIL_SERVER'),
                'MAIL_PORT': os.getenv('OUTLOOK_MAIL_PORT'),
                'MAIL_USERNAME': os.getenv('OUTLOOK_MAIL_USERNAME'),
                'MAIL_PASSWORD': os.getenv('OUTLOOK_MAIL_PASSWORD'),
                'MAIL_USE_TLS': os.getenv('OUTLOOK_MAIL_USE_TLS') == 'True',
                'MAIL_USE_SSL': os.getenv('OUTLOOK_MAIL_USE_SSL') == 'True'
            }
        }


        if provider in MAIL_SERVERS:
            app.config.update(MAIL_SERVERS[provider])
        else:
            raise ValueError("Provider not supported")

    def get_secret_key(self):
        """Retorna a SECRET_KEY."""
        return os.getenv('SECRET_KEY', 'default_secret_key')
    
    def get_database_config(self):
        """Retorna a configuração do banco de dados."""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_DATABASE', 'cs50')
        }

    def get_database_uri(self):
        """Retorna o URI do banco de dados para SQLAlchemy."""
        db_config = self.get_database_config()
        return f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

    def init_app(self, app):
        self.get_set_email(app, 'gmail')

        """Configura a aplicação Flask com as variáveis definidas."""
        app.config['SECRET_KEY'] = self.get_secret_key()
        # app.config['SQLALCHEMY_DATABASE_URI'] = self.get_database_uri()
        # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
        # Inicializa outras configurações com valores padrão
        app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
        app.config['TESTING'] = os.getenv('TESTING', 'False') == 'True' 
        app.config['LOGGING_LEVEL'] = os.getenv('LOGGING_LEVEL', 'DEBUG')

        # Configurações de sessão
        app.config['SESSION_COOKIE_NAME'] = os.getenv('SESSION_COOKIE_NAME', 'your_session_cookie_name')
        app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True' 
        
        # Converte os valores de dias para timedelta
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=int(os.getenv('PERMANENT_SESSION_LIFETIME', 5)))
        app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=int(os.getenv('REMEMBER_COOKIE_DURATION', 30)))
        
        # app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', '/path/to/upload')
        app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)) 


        app.config['BABEL_DEFAULT_LOCALE'] = os.getenv('BABEL_DEFAULT_LOCALE', 'en')
