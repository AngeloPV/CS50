from flask import request, session

from ...renderer import template_render
from ...models.Register_user import Register_user

class Register:
    def __init__(self):
        # Inicialize qualquer atributo necessário aqui
        self.register = Register_user()  # Exemplo: inicializa um objeto da classe MDRegister
            
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

                    if self.register.addUser(form_data):
                        if "error_validate" in session:
                            del(session["error_validate"])

                        return template_render("verify.html", register_email=True)
                    elif "error_validate" in session:
                        form_data['ConfirmPass'] = form_data['password']
                        print(session["error_validate"])
                        form_data["error_message"] = session["error_validate"]

                        return template_render("register.html", **form_data)
                    elif "Error_send_email" in session:

                        form_data['ConfirmPass'] = form_data['password']
                        form_data["error_message"] = session["error_send_email"]
                        return template_render("register.html", **form_data)
                
                form_data["error_message"] = {'password': 'The password field and password confirmation must be the same.'}
                return template_render("register.html", **form_data)
            else:
                form_data["error_message"] = {'all': 'All fields must be filled in.'}
                return template_render("register.html", **form_data)
        else:
            return template_render("register.html")
