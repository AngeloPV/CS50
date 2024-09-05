# CryptoExchange Platform

<p>Uma plataforma segura e intuitiva que permite aos usuários acessar o mercado de criptomoedas para comprar, vender e trocar criptomoedas populares como <strong>Bitcoin (BTC)</strong> e <strong>Ethereum (ETH)</strong>.</p>

## 🚀 Funcionalidades Principais

<ul>
  <li><strong>Criação de Conta & Login Seguro:</strong> Oferece um processo de registro e autenticação para garantir a privacidade e segurança dos usuários.</li>
  <li><strong>Compra e Venda de Criptomoedas:</strong> Permite a negociação de Bitcoin e Ethereum diretamente através da plataforma.</li>
  <li><strong>Visualização de Saldos:</strong> Interface amigável para os usuários visualizarem suas contas e acompanharem seus saldos em diferentes criptomoedas.</li>
  <li><strong>Histórico de Transações:</strong> Acompanhe todas as compras, vendas e trocas realizadas.</li>
  <li><strong>Segurança de Transações:</strong> As transações são protegidas com padrões avançados de segurança para garantir a integridade dos dados e dos fundos dos usuários.</li>
</ul>

## 🎯 Objetivos Específicos

<ul>
  <li><strong>Criação de Contas & Login Seguro:</strong> Proporcionar um sistema de autenticação seguro para proteger as credenciais e os dados dos usuários.</li>
  <li><strong>Compra e Venda de Criptomoedas:</strong> Implementar as funcionalidades básicas para comprar, vender e trocar Bitcoin e Ethereum.</li>
  <li><strong>Interface de Usuário Amigável:</strong> Desenvolver uma interface intuitiva que permite visualizar facilmente saldos e transações.</li>
  <li><strong>Segurança Robusta:</strong> Garantir a proteção das transações e dos dados dos usuários com criptografia e autenticação multi-fator.</li>
</ul>

## 🛠️ Tecnologias Utilizadas

<ul>
  <li><strong>Backend:</strong> Flask</li>
  <li><strong>Banco de Dados:</strong> Pymysql</li>
  <li><strong>Autenticação:</strong> OAuth2 / JWT (em desenvolvimento)</li>
  <li><strong>Frontend:</strong> HTML5, CSS3, JavaScript</li>
  <li><strong>Criptomoedas Suportadas:</strong> Bitcoin (BTC), Ethereum (ETH)</li>
</ul>

## 🚧 Em Desenvolvimento

<ul>
  <li>Implementação da autenticação com OAuth2</li>
  <li>Integração com APIs de criptomoedas em tempo real</li>
  <li>Suporte a mais criptomoedas no futuro</li>
  <li>Implementação de uma carteira segura</li>
</ul>

## 📝 Instalação

<ol>
  <li>Instale as dependências com o <a href="https://python-poetry.org/" target="_blank">Poetry</a>:
    <pre><code>poetry install</code></pre>
  </li>
  <li>Configure as variáveis de ambiente no arquivo <code>.env</code>.</li>
  <li>Execute a aplicação:
    <pre><code>poetry run flask run</code></pre>
  </li>
  <li>Crie o repositório poetry:
    <pre><code>peotry new my_project</code></pre>
  </li>
  <li>Clone o repositório dentro do poetry:
    <pre><code>git clone https://github.com/AngeloPV/CS50.git</code></pre>
  </li>
</ol>


## 🔧 Configurando o Arquivo .env

<p>Este projeto utiliza um arquivo <code>.env</code> para armazenar variáveis de ambiente essenciais que configuram a aplicação. Essas variáveis são usadas para definir chaves secretas, parâmetros de sessão, configurações de banco de dados, e-mail e outras informações sensíveis. O arquivo <code>.env</code> não é incluído no controle de versão (está listado no <code>.gitignore</code>) para proteger essas informações.</p>
Estrutura do arquivo .env

### Variáveis de ambiente para serem usadas em todo o código do seu projeto
<pre><code>
# Configurações do Flask
SECRET_KEY=afdes123
DEBUG=True
TESTING=False
LOGGING_LEVEL=DEBUG

# Configurações de sessão
SESSION_COOKIE_NAME=coockie_AF
SESSION_COOKIE_SECURE=True
PERMANENT_SESSION_LIFETIME=5  # em dias
REMEMBER_COOKIE_DURATION=30  # em dias

# Configuração para uploads
UPLOAD_FOLDER=/path/to/upload
MAX_CONTENT_LENGTH=16777216  # 16 MB

# Internacionalização
BABEL_DEFAULT_LOCALE=en

# Configuração do banco de dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_DATABASE=cs50

# Configurações de e-mail
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=43e6e4f4e74b0c
MAIL_PASSWORD=717f977164cfcc
MAIL_USE_TLS=True
MAIL_USE_SSL=False
</code></pre>


### Carregar as Variáveis de Ambiente no Código
<p>Para garantir que as variáveis de ambiente sejam carregadas corretamente, o projeto utiliza a biblioteca <a href="https://pypi.org/project/python-dotenv/" target="_blank">python-dotenv</a>. Abaixo está um exemplo de como fazer isso no arquivo <code>app.py</code>:</p>

<pre><code>from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Exemplo de acesso a uma variável
secret_key = os.getenv("SECRET_KEY")
database_host = os.getenv("DB_HOST")
</code></pre>

## 🔧 Configurando o Arquivo `.flaskenv`

<p>O arquivo <code>.flaskenv</code> é utilizado para definir variáveis de ambiente específicas para o Flask. Este arquivo facilita a configuração do ambiente de desenvolvimento e pode ser usado para definir a aplicação Flask principal, o ambiente e arquivos adicionais que devem ser monitorados. O arquivo <code>.flaskenv</code> também não é incluído no controle de versão (está listado no <code>.gitignore</code>) para proteger essas configurações específicas.</p>

### Estrutura do arquivo `.flaskenv`

<p>Aqui está um exemplo de como o arquivo <code>.flaskenv</code> deve ser configurado:</p>
<pre><code># Configuração do Flask
FLASK_APP=src.finalProject.app:app
FLASK_ENV=development
FLASK_RUN_EXTRA_FILES=src/finalProject/templates/*.html
</code></pre>

### Explicação das Variáveis

<ul>
  <li><strong>FLASK_APP:</strong> Define o módulo da aplicação Flask. Neste caso, está configurado para <code>src.finalProject.app:app</code>, onde <code>app</code> é o objeto Flask.</li>
  <li><strong>FLASK_ENV:</strong> Define o ambiente do Flask. <code>development</code> configura o Flask para o modo de desenvolvimento, que inclui recarregamento automático e detalhes de erro mais detalhados.</li>
  <li><strong>FLASK_RUN_EXTRA_FILES:</strong> Lista arquivos adicionais que devem ser monitorados pelo Flask. Qualquer alteração nesses arquivos causará uma reinicialização automática da aplicação.</li>
</ul>

## 🤝 Contribuições

<p>Contribuições são bem-vindas! Sinta-se à vontade para abrir uma <i>issue</i> ou enviar um <i>pull request</i>.</p>
