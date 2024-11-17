# outro_arquivo.py
from finalProject.tests.dependencies import import_components
from dotenv import load_dotenv

# Dicionário de módulos e componentes a importar
modules_and_components = {
    'datetime': ['datetime'],
    "os": ['os'],
}

# Importa os componentes
components = import_components(modules_and_components)

now = components.get('datetime', {}).get('datetime')
print(components)
# Carregar variáveis do arquivo .env
load_dotenv()

# # Acessar variáveis de ambiente
# database_url = os.getenv("DATABASE_URL")
# secret_key = os.getenv("SECRET_KEY")
# print(database_url)


a = now.now()
# Acessa o componente específico
Blueprint = components.get('flask', {}).get('Blueprint')

if Blueprint:
    # Use o Blueprint
    example_bp = Blueprint('example', __name__)