from flask import request, session
from ..renderer import template_render
from ..models.register_user import register_user

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

            if(condition and form_data['ConfirmPass'] == form_data['password'] ):
                del(form_data["ConfirmPass"])

                if self.obj.addUser(form_data):
                    return template_render("index.html", **form_data)
                # elif session["Error_send_email"]:
                #     return session["Error_email"] 
                # elif session["Error_con"]:
                #     return session["Error_con"]
                else:
                    return "a" 
            else:
                return template_render("register.html", **form_data)
        else:
            return template_render("register.html")


# def validateEmail():

