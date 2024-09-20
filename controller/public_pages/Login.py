from flask import request, redirect, url_for, session

from ...renderer import template_render
from ...models.Login_user import Login_user
# A fazer:
# 1. Fazer a pagina pra quando o usaruio acessar pelo email, quando aceessar atualizar o banco email_sit
# Depois no Lohin verificar se o usario esta com a conta autorizada ja
class Login:
    def __init__(self):
        # Inicialize qualquer atributo necessário aqui
        self.login = Login_user()  # Exemplo: inicializa um objeto da classe MDRegister

    def index(self):
        if request.form.get("SendLogin"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["SendLogin"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                if self.login.verify_login(form_data):
                    return redirect(url_for("main_routes.route_method", route_name="dashboard", method="index"))

                form_data["error_message"] = session["error_message"]
                del(session["error_message"])
                return template_render("login.html", **form_data)

            form_data["error_message"] = "Todos os campos devem ser preenchidos!!"
            return template_render("login.html", **form_data)

        else:
            if 'Authorize' in session:
                authorize = session['Authorize']
                
                del session['Authorize']

                return template_render("login.html", authorize=authorize)

            return template_render("login.html")
