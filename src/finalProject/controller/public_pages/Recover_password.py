from flask import request, session

from ...renderer import template_render
from ...models.Resend_Password import Resend_Password


class Recover_password:
    """
    Classe responsavel por solicitar a recuperação de senha
    """

    def __init__(self):
        self.new_password = Resend_Password()
            
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
                # return template_render("recover_password.html", register_email=True
                if self.new_password.verify_email_recover(form_data):
                    session['user_email'] = form_data['email']
                    return template_render("verify.html", Recover_password=True)
                
                 # Se ocorrer um erro de validação, exibe uma mensagem de erro e renderiza a página de reenvio
                elif "error_validate" in session:
                    form_data["error_message"] = session["error_validate"]
                    del(session["error_validate"])  # Remove a mensagem de erro da sessão
                    return template_render("recover_password.html", **form_data)

                # Se ocorrer um erro ao tentar enviar o email, exibe uma mensagem de erro
                elif "error_send_email" in session:
                    form_data["error_message"] = session["error_send_email"]
                    del(session["error_send_email"])  # Remove a mensagem de erro da sessão
                    return template_render("recover_password.html", **form_data)
            else:
                form_data["error_message"] = "Todos os campos devem ser preenchidos!!"
                return template_render("recover_password.html", **form_data)
        else:
            return template_render("recover_password.html")

    
