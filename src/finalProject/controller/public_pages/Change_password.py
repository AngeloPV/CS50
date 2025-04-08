from flask import request, session, redirect, url_for

from ...renderer import template_render
from ...models.Resend_Password import Resend_Password
from .Error import Error
from ...models.Update_password import Update_password

class Change_password:
    """
    Classe responsavel por solocitar a troca de senha do usuario
    """

    def __init__(self):
        self.new_password = Resend_Password()
        self.erro = Error()
        self.update_pass = Update_password() 
            
    def index(self, code):
        print(code, session.get('code'))
        """
        Função responsavel por validar as informações do formulário e redireciona para a página de 
        login, caso contrario retrorna erro
        """
        if not session.get('code') or code != session['code']:
            return self.erro.show_error('Page not found', 500)

        if request.form.get("SendNewPassword"):

            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["SendNewPassword"])

            condition = True
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            if condition:
                # Verifica se as senhas sao iguais
                if form_data['ConfirmPass'] == form_data['password']:
                    del(form_data["ConfirmPass"])

                    if self.update_pass.new_password(form_data['password']):
                        if "error_validate" in session:
                            del(session["error_validate"])

                        session['Change_password'] = True  # Marca a conta como autorizada
                        return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
                    
                    # Se houve erro de validação, renderiza novamente o formulário de registro com a mensagem de erro
                    elif "error_validate" in session:
                        form_data['ConfirmPass'] = form_data['password']  # Restaura o campo 'ConfirmPass'
                        form_data["error_message"] = session["error_validate"]['password']
                        del(session["error_validate"])

                        return template_render("Change_Password.html", **form_data)
                    else:
                        form_data['ConfirmPass'] = form_data['password']  # Restaura o campo 'ConfirmPass'
                        form_data["error_message"] = 'Unexpected error occurred, if it persists, contact us!'

                        return template_render("Change_Password.html", **form_data)


                # Se a senha e a confirmação de senha não coincidirem, exibe a mensagem de erro
                form_data["error_message"] = 'The password field and password confirmation must be the same.'
                return template_render("Change_Password.html", **form_data)
            else: 
                form_data["error_message"] = 'All fields must be filled in'
                return template_render("Change_Password.html", **form_data)
        else:
            return template_render("Change_password.html")

