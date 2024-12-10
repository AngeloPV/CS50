from ..app import app
from .helper_select import Select
from .helper_insert import Insert
from .generate_code import generate_random_code
from ..config import Config

from flask import session
from flask_mail import Mail, Message  # type: ignore
from premailer import Premailer  # type: ignore


class Send_Email():
    def __init__(self):
        """
        Inicializa as instâncias necessárias para o envio de e-mails.

        Atributos:
            select (Select): Instância da classe Select para consultas ao banco.
            insert (Insert): Instância da classe Insert para inserções no banco.
            mail (Mail): Instância do objeto Mail para envio de e-mails.
            code (str): Código gerado aleatoriamente.
            email_config (Config): Configurações de e-mail.
            content_html (str): Conteúdo HTML do e-mail.
            content_text (str): Conteúdo texto do e-mail.
            result (bool): Resultado da execução do envio de e-mail.
        """
        self.select = Select()
        self.insert = Insert()
        self.mail = Mail(app)
        self.code = generate_random_code(6)  # Gera um código aleatório
        self.email_config = Config()  # Configurações de e-mail

        self.content_html = ""
        self.content_text = ""
        self.result = None

    def get_code(self):
        """
        Retorna o código gerado.

        Retorna:
            str: O código gerado.
        """
        return self.code
    
    def config_email(self, id_email, data, url, type='text', to_update=''):
        """
        Configura o e-mail e envia para o destinatário.

        Parâmetros:
            id_email (int): ID do e-mail a ser enviado.
            data (dict): Dados do usuário (como nome, e-mail, etc).
            url (str): URL a ser inserida no corpo do e-mail.
            type (str, opcional): Tipo de e-mail ('text' ou 'code'). O padrão é 'text'.

        Retorna:
            bool: True se o e-mail for enviado com sucesso, False caso contrário.
        """
        self.id_email = id_email
        self.url = url
        self.data = data
        self.type = type

        # Validação dos dados fornecidos
        if not self.data.get("name"):
            self.data["name"] = "Dear Customer"

        if not self.data.get("verify") or not self.data.get("email"):
            session["Error_send_email"] = "The fields 'verify' and 'email' are required"

            return False
        
        # Recupera os dados do template do e-mail
        self.select.exe_select("SELECT content_html, content_text, subject, type FROM email_data WHERE id = %s LIMIT %s", 
                               f'{{"id": "{self.id_email}", "LIMIT": "1"}}', False)
        self.result = self.select.get_result()

        
       
        if self.result:
            self.email_html()  # Prepara o conteúdo HTML do e-mail
            self.email_text()  # Prepara o conteúdo texto do e-mail

            try:
                # Envia o e-mail
                with app.app_context():
                    msg = Message(self.result[2]+f' {to_update}',# Assunto do e-mail
                                  sender='noereply@gmail.com',
                                  recipients=[self.data["email"]])
                    msg.body = self.content_text
                    msg.html = self.content_html
                    self.mail.send(msg)

                    print("E-mail enviado com sucesso!")
                    if self.insert_email_sit():  # Insere a situação do e-mail na tabela
                        return True
                    return False
            except Exception as e:
                print(str(e))  # Imprime o erro
                session["error_send_email"] = str(e)
                return False

        session["error_send_email"] = "Error: unable to perform the Select"

        return False

    def email_text(self):
        """
        Converte o conteúdo do e-mail para o formato de texto simples.

        Retorna:
            None
        """
        self.content_text = self.result[1].split('//')

        result_text = f"Hello, {self.data['name']}\n\n"
        for value in self.content_text:
            if value == "URL":
                value = f'\nhttp://127.0.0.1:5000/{self.url}{self.data["verify"]}"\n'
            elif value == "Sincerely,":
                result_text += f"{value}\n"
                continue  

            result_text += f"{value}\n\n"

        self.content_text = result_text

    def email_html(self):
        """
        Converte o conteúdo do e-mail para o formato HTML, aplicando o estilo adequado.

        Retorna:
            None
        """
        # CSS customizado para os tipos de conteúdo (botão ou código)
        validate_button_css = """
        .validation-button {
            display: inline-block;
            background-color: #ff6f3c;
            color: white;
            text-decoration: none;
            padding: 10px 20px; 
            border-radius: 4px; 
            font-weight: bold; 
            margin: 20px 0;
        }
        .validation-button:hover {
            background-color: #e55b28;
        }
        """

        validate_code_css = """
        .code {
            padding: 10px;
            text-align: center;
            margin: 0 auto;
        }

        .code_digit {
            width: 40px;
            height: 40px;
            display: inline-block; 
            background-color: #f4f4f4;
            border: 1px solid #ccc;
            font-size: 20px;
            border-radius: 4px;
            margin: 0 5px; 
            padding-bottom: 2%;
        }
        """

        # Adiciona o CSS necessário dependendo do tipo do e-mail
        extra_css = ''
        if self.type == 'code':
            extra_css = validate_code_css
        elif self.type == 'button':
            extra_css = validate_button_css

        # CSS padrão para o corpo do e-mail
        css = f"""
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                background-color: #ffffff;
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background-color: #1b263b;
                padding: 20px;
                text-align: center;
                color: white;
                border-radius: 8px 8px 0 0;
            }}
            .email-header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .email-content {{
                padding: 20px;
                color: #343a40;
                line-height: 1.6;
            }}
            .email-footer {{
                text-align: center;
                font-size: 12px;
                color: #343a40;
                margin-top: 20px;
            }}
            .email-footer p {{
                margin: 0;
            }}
            {extra_css}
        </style>
        """

        # Monta o conteúdo HTML do e-mail
        result_html = f"""
        <html>
        <head>
            {css}
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>Welcome to AF Crypto!</h1>
                </div>
                <div class="email-content">
                    <h3>Hello, {self.data['name'].capitalize()}</h3>
        """

        for value in self.result[0].split('//'):
            if value == "CODE" and self.type == "code":
                value = '<div class="code">'
                for digit in self.code:
                    value += f'<span class="code_digit">{digit}</span>'
                value += '</div>'
            if value == "URL" and self.type == "button":
                value = f'<p><a href="http://127.0.0.1:5000/{self.url}{self.data["verify"]}" class="validation-button">Acessar Link</a></p>'
            result_html += f"<p>{value}</p>"

        result_html += """
                </div>
                <div class="email-footer">
                    <p>If you have not performed any action related to Company AF, please disregard this email.</p>
                    <p>Thank you for choosing Company AF!</p>
                </div>
            </div>
        </body>
        </html>
        """

        premailer = Premailer(result_html)
        inlined_html = premailer.transform()
        self.content_html = inlined_html

    def insert_email_sit(self):
        """
        Insere a situação do envio de e-mail na tabela email_sit.

        Retorna:
            bool: True se a inserção for bem-sucedida, False caso contrário.
        """
        self.select.exe_select("""SELECT id FROM email_sit WHERE email_id = %s AND user_id = %s AND email_sit = %s
                                LIMIT %s""", f'{{"email_id": "{self.id_email}", "user_id": "{self.data["id"]}", "email_sit": "1", "LIMIT": "1"}}', True)

        if self.select.get_result():
            return True

        data = {"email_id": self.id_email, "user_id": self.data["verify"], "email_sit": 1} if not self.data.get("id") else {"email_id": self.id_email, "user_id": self.data["id"],  "email_sit": 1}
        
        self.insert.exe_insert(data, "email_sit", close_conn=True)
        result_insert = self.insert.getResult()

        return result_insert if result_insert else False
