from flask import request, session

from ...renderer import template_render
from ...models.register_user import register_user

class Register:
    def __init__(self):
        # Inicialize qualquer atributo necessário aqui
        self.obj = register_user()  # Exemplo: inicializa um objeto da classe MDRegister
            
    def index(self):
        if request.form.get("SendRegister"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["SendRegister"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                if form_data['ConfirmPass'] == form_data['password']:
                    del(form_data["ConfirmPass"])

                    if self.obj.addUser(form_data):
                        return template_render("login.html", register_email=True)
                    elif "error_validate" in session:
                        form_data['ConfirmPass'] = form_data['password']
                        print(session["error_validate"])
                        return template_render("register.html", **form_data)
                    elif "Error_send_email" in session:
                        print(session["error_send_email"]) 
                        form_data['ConfirmPass'] = form_data['password']
                        return template_render("register.html", **form_data)
                
                form_data["error_message"] = "O campo senha e a confirmação de senha devem ser iguais"
                return template_render("register.html", **form_data)
            else:
                form_data["error_message"] = "Todos os campos devem ser preenchidos!!"
                return template_render("register.html", **form_data)
        else:
            return template_render("register.html")

    
