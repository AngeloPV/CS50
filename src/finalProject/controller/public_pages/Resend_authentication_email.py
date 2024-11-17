from flask import request, session

from ...renderer import template_render
from ...models.Resend_authenticate import Resend_authenticate


class Resend_authentication_email:
    def __init__(self):
        # Inicialize qualquer atributo necessário aqui
        self.resend = Resend_authenticate()  # Exemplo: inicializa um objeto da classe MDRegister
            
    def index(self):
        if request.form.get("ResendAuthorize"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário

            del(form_data["ResendAuthorize"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                if self.resend.verify_email(form_data):
                    return template_render("verify.html", register_email=True)
                elif "error_validate" in session:
                    print(session["error_validate"])
                    form_data["error_message"] = session["error_validate"]
                    return template_render("resend_authentication_email.html", **form_data)
                elif "error_send_email" in session:
                    form_data["error_message"] = session["error_send_email"]
                    return template_render("resend_authentication_email.html", **form_data)
            else:
                form_data["error_message"] = "All fields must be filled in!"
                return template_render("resend_authentication_email.html", **form_data)
        else:
            return template_render("resend_authentication_email.html")

    
