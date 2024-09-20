from flask import request, session

from ...renderer import template_render
from ...models.register_user import register_user

class Resend_authentication_email:
    def __init__(self):
        # Inicialize qualquer atributo necessário aqui
        self.obj = register_user()  # Exemplo: inicializa um objeto da classe MDRegister
            
    def index(self):
        if request.form.get("ResendAuthorize"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["ResendAuthorize"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                return template_render("resend_authentication_email.html", register_email=True)
            else:
                form_data["error_message"] = "Todos os campos devem ser preenchidos!!"
                return template_render("resend_authentication_email.html", **form_data)
        else:
            return template_render("resend_authentication_email.html")

    
