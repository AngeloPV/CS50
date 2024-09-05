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
  <li>Clone o repositório:
    <pre><code>git clone https://github.com/username/crypto-exchange-platform.git</code></pre>
  </li>
  <li>Instale as dependências com o <a href="https://python-poetry.org/" target="_blank">Poetry</a>:
    <pre><code>poetry install</code></pre>
  </li>
  <li>Configure as variáveis de ambiente no arquivo <code>.env</code>.</li>
  <li>Execute a aplicação:
    <pre><code>poetry run flask run</code></pre>
  </li>
</ol>


## 🔧 Configurando o Arquivo .env

<p>Este projeto utiliza um arquivo <code>.env</code> para armazenar variáveis de ambiente essenciais que configuram a aplicação. Essas variáveis são usadas para definir chaves secretas, parâmetros de sessão, configurações de banco de dados, e-mail e outras informações sensíveis. O arquivo <code>.env</code> não é incluído no controle de versão (está listado no <code>.gitignore</code>) para proteger essas informações.</p>
Estrutura do arquivo .env
<p>Aqui está um exemplo de como o arquivo <code>.env</code> deve ser configurado:</p><pre><code># Variáveis de ambiente para serem usadas em todo o código do seu projeto <br># Configurações do Flask SECRET_KEY=afdes123 <br>DEBUG=True <br>TESTING=False <br>LOGGING_LEVEL=DEBUG <br># Configurações de sessão <br>SESSION_COOKIE_NAME=coockie_AF <br>SESSION_COOKIE_SECURE=True <br>PERMANENT_SESSION_LIFETIME=5 # em dias <br>REMEMBER_COOKIE_DURATION=30 # em dias <br># Configuração para uploads <br>UPLOAD_FOLDER=/path/to/upload <br>MAX_CONTENT_LENGTH=16777216 # 16 MB # Internacionalização <br>BABEL_DEFAULT_LOCALE=en <br># Configuração do banco de dados <br>DB_HOST=localhost <br>DB_USER=root <br>DB_PASSWORD= DB_DATABASE=cs50 <br># Configurações de e-mail <br>MAIL_SERVER=sandbox.smtp.mailtrap.io <br>MAIL_PORT=2525 <br>MAIL_USERNAME=43e6e4f4e74b0c <br>MAIL_PASSWORD=717f977164cfcc <br>MAIL_USE_TLS=True MAIL_USE_SSL=False </code></pre>
Detalhes das Variáveis
<ul> <li><strong>SECRET_KEY</strong>: Protege dados como sessões e tokens de CSRF. É fundamental manter esta chave em segredo.</li> <li><strong>DEBUG</strong>: Defina como <code>True</code> para desenvolvimento e <code>False</code> em produção.</li> <li><strong>SESSION_COOKIE_SECURE</strong>: Garante que os cookies de sessão só sejam transmitidos via HTTPS (mantenha <code>False</code> durante o desenvolvimento).</li> <li><strong>UPLOAD_FOLDER</strong>: Defina o caminho onde os arquivos enviados serão armazenados.</li> <li><strong>DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE</strong>: Informações de conexão com o banco de dados.</li> <li><strong>MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD</strong>: Configurações para enviar e-mails através de um servidor SMTP. É recomendado usar um serviço de sandbox (como Mailtrap) durante o desenvolvimento.</li> </ul>
Carregar as Variáveis de Ambiente no Código
<p>Para garantir que as variáveis de ambiente sejam carregadas corretamente, o projeto utiliza a biblioteca <a href="https://pypi.org/project/python-dotenv/" target="_blank">python-dotenv</a>. Abaixo está um exemplo de como fazer isso no arquivo <code>app.py</code>:</p> <pre><code>from dotenv import load_dotenv import os # Carregar variáveis do arquivo .env load_dotenv() # Exemplo de acesso a uma variável secret_key = os.getenv("SECRET_KEY") database_host = os.getenv("DB_HOST") </code></pre> <p>Com isso, as variáveis de ambiente serão corretamente carregadas na sua aplicação.</p>


## 🤝 Contribuições

<p>Contribuições são bem-vindas! Sinta-se à vontade para abrir uma <i>issue</i> ou enviar um <i>pull request</i>.</p>
