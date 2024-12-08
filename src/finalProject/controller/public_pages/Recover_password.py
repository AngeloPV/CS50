from flask import request, session

from ...renderer import template_render
from ...models.Register_user import Register_user

class Recover_password:
    """
    Classe responsavel por solicitar a recuperação de senha
    """
            
    def index(self):
        """
        Função responsavel por validar as informações do formulário e redireciona para a página de 
        recuperação com o valor register_email como true para que seja autorizado a solicitação 
        da recuperação, em caso de erro retrorna erro
        """
        if request.form.get("SendRecover"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["SendRecover"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                return template_render("recover_password.html", register_email=True)
            else:
                form_data["error_message"] = "Todos os campos devem ser preenchidos!!"
                return template_render("recover_password.html", **form_data)
        else:
            return template_render("recover_password.html")

    
