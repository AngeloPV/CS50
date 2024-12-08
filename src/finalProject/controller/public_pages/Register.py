from flask import request, session

from ...renderer import template_render
from ...models.Register_user import Register_user

class Register:
    """
    Classe responsavel por efetuar o registro do usuario.

    A classe lida com o recebimento de dados de registro, validação dos dados inseridos,
    e a interação com o modelo de dados para adicionar o novo usuário ao sistema.

    """
    def __init__(self):
        self.register = Register_user() #instancia a classe responsavel pela manipulação de dados no registro
            
    def index(self):
        """
        Processa os dados de registro do usuário. Quando o formulário de registro é enviado,
        ele valida os campos, verifica se a senha e a confirmação de senha são iguais, 
        e tenta adicionar o novo usuário ao banco de dados.

        Retorna: Se o registro for bem-sucedido, renderiza a página de verificação de e-mail.
                Se houver erros de validação, renderiza o formulário de registro com mensagens de erro.
        """
        if request.form.get("SendRegister"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            
            del(form_data["SendRegister"])

            condition = True
            # Verifica se todos os campos do formulário foram preenchidos
            for camp in form_data:
                if not form_data[camp]:
                    condition = False
            # Verifica se os dados sao validos
            if condition:
                # Verifica se as senhas sao iguais
                if form_data['ConfirmPass'] == form_data['password']:
                    del(form_data["ConfirmPass"])

                    if self.register.addUser(form_data):
                        if "error_validate" in session:
                            del(session["error_validate"])

                        return template_render("verify.html", register_email=True)
                    
                    # Se houve erro de validação, renderiza novamente o formulário de registro com a mensagem de erro
                    elif "error_validate" in session:
                        form_data['ConfirmPass'] = form_data['password']  # Restaura o campo 'ConfirmPass'
                        form_data["error_message"] = session["error_validate"]
                        del(session["error_validate"])

                        return template_render("register.html", **form_data)

                    # Se houve erro ao enviar o e-mail de verificação, exibe a mensagem de erro
                    elif "Error_send_email" in session:
                        form_data['ConfirmPass'] = form_data['password']
                        form_data["error_message"] = session["error_send_email"]
                        return template_render("register.html", **form_data)
                
                # Se a senha e a confirmação de senha não coincidirem, exibe a mensagem de erro
                form_data["error_message"] = {'password': 'The password field and password confirmation must be the same.'}
                return template_render("register.html", **form_data)
            else:
                # Se algum campo estiver vazio, exibe a mensagem de erro
                form_data["error_message"] = {'all': 'All fields must be filled in.'}
                return template_render("register.html", **form_data)
        else:
            # Se o formulário não for enviado, renderiza o formulário de registro vazio
            return template_render("register.html")