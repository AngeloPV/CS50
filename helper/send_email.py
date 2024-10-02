from ..app import app
from .helper_select import Select
from .helper_insert import Insert
from .generate_code import generate_random_code

from flask import session
from flask_mail import Mail, Message # type: ignore


class Send_Email():
    def __init__(self):
        self.select = Select()
        self.insert = Insert()
        self.mail = Mail(app)
        #Gera o código
        self.code = generate_random_code(6)

        self.content_html = ""
        self.content_text = ""  
        self.result = None

    def get_code(self):
        return self.code
    
    def config_email(self, id_email, data, url, type='text'):
        self.id_email = id_email
        self.url = url
        self.data = data
        self.type = type

        print(self.data)
        if not self.data.get("name"):
            self.data["name"] = "Caro Cliente"

        if not self.data.get("verify") or not self.data.get("email"):
            session["Error_send_email"] = "Precisar passar o campo verify e email"
            return False
        

        self.select.exe_select("SELECT content_html, content_text, subject, type FROM email_data WHERE id = %s LIMIT %s", f'{{"id": "{self.id_email}", "LIMIT": "1"}}', True)

        self.result = self.select.get_result()

        # print(self.result)

        if(self.result):
            self.email_html()
            self.email_text()

            # Chamada da função em um contexto apropriado
            try:
                with app.app_context():
                    msg = Message(self.result[2],
                                  sender='noreply@yourdomain.com',
                                  recipients=[self.data["email"]])
                    msg.body = self.content_text
                    msg.html = self.content_html
                    self.mail.send(msg)

                    print("E-mail enviado com sucesso!")   
                    if(self.insert_email_sit()): 
                        return True
                    
                    return False
            except Exception as e:
                # Captura e imprime qualquer erro que ocorra
                session["error_send_email"] = e
                return False
            
        session["error_send_email"] = "Error: não foi possivel relizar o Select"
        return False


    def email_text(self):
        self.content_text = self.result[1].split('//')

        result_text = f"Olá, {self.data['name']}\n\n"
        for value in self.content_text:
            if value == "URL":
                value = f'\nhttp://127.0.0.1:5000/{self.url}{self.data["verify"]}"\n'
            elif value == "Atenciosamente,":
                result_text += f"{value}\n"
                continue  

            result_text += f"{value}\n\n"

        self.content_text = result_text


    def email_html(self):
        # Define o CSS do botao de validate
        validate_button_css = """.validation-button {
                display: inline-block;
                background-color: #ff6f3c; /* Laranja */
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                margin: 20px 0;
            }
            .validation-button:hover {
                background-color: #e55b28; /* Tom mais escuro de laranja para hover */
            }"""
        
        # Define o CSS do codigo de validate
        validate_code_css = """.code{
                padding: 2.5vh;
                display: flex;
                justify-content: center;
                gap: 1vh;
                align-items: center;
                margin: 0 auto;
            }
            
            .code_digit {
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #f4f4f4;
                border: 1px solid #ccc;
                font-size: 20px;
                border-radius: 4px;
            }
            """
        #define os codigos extra que vao ser adicionados ao css padrao
        extra_css = ''
        if self.type == 'code':
            extra_css = validate_code_css
        elif self.type == 'button':
            extra_css = validate_button_css

        # Define o CSS padrao do email

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
                background-color: #1b263b; /* Azul escuro */
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
                color: #343a40; /* Cinza escuro */
                line-height: 1.6;
            }}
            .email-content p {{
                margin: 10px 0;
            }}
    
            {extra_css}
            .email-footer {{
                text-align: center;
                font-size: 12px;
                color: #343a40; /* Cinza escuro */
                margin-top: 20px;
            }}
            .email-footer p {{
                margin: 0;
            }}
        </style>
        """

        # Monta o conteúdo HTML
        result_html = f"""
        <html>
        <head>
            {css}
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>Bem Vindo AF Crypto!</h1>
                </div>
                <div class="email-content">
        """

        result_html += f"<h3>Olá, {self.data['name'].capitalize()}</h3>"

        for value in self.result[0].split('//'):
            #verifica se o marcador é CODE ou URL e substitui pelo valor adequado
            if value == "CODE" and self.type == "code":

                #Cria a div
                value = f'<div class="code">'
                #Separa cada digito individualmente
                for digit in self.code:
                    value += f'<span class="code_digit">{digit}</span>'
                #Fecha a div
                value += '</div>'
            if value == "URL" and self.type == "button":
                value = f'<p><a href="http://127.0.0.1:5000/{self.url}{self.data["verify"]}" class="validation-button">Acessar Link</a></p>'
            result_html += f"<p>{value}</p>"

        result_html += """
                </div>
                <div class="email-footer">
                    <p>Se você não tiver realizado qualquer ação relacionada à Empresa AF, por favor, desconsidere este e-mail..</p>
                    <p>Obrigado por escolher a Empresa AF!</p>
                    <p>Estamos à disposição em nosso local de contato.</p>
                </div>
            </div>
        </body>
        </html>
        """
        self.content_html = result_html
        # Insere o conteúdo gerado no template HTML


    def insert_email_sit(self):
        if not self.data.get("id"):
            data = {"email_id": self.id_email, "user_id": self.data["verify"], "email_sit": 1}
        elif self.data.get("id"):
            data = {"email_id": self.id_email, "user_id": self.data["id"],  "email_sit": 1}
        
        self.insert.exe_insert(data, "email_sit", close_conn=True)
        
        result_insert = self.insert.getResult()

        if(result_insert):
            return True
        else:
            session["error_send_email"] = "Error: não foi possivel relizar o Insert"
            return False
        