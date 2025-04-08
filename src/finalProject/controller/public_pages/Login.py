from flask import request, redirect, url_for, session

from ...renderer import template_render
from ...models.Login_user import Login_user

class Login:
    """
    Classe responsável pelo gerenciamento do processo de login de usuários.
    Contém a lógica de verificação de login, validação de formulários e controle de sessões.

    Parametros:
        login: Instância da classe Login_user, responsável pela verificação das credenciais de login.
    """
    def __init__(self):
        self.login = Login_user()  #instancia a classe responsavel pelo login

    def index(self):
        """
        Processa o formulário de login enviado pelo usuário, verificando as credenciais e redirecionando 
        para a página adequada. Também lida com mensagens de erro e campos obrigatórios.

        retorna: redirecionamento para a página do dashboard se o login for bem-sucedido, ou renderização da página de login com mensagens de erro.
        """

        # Verifica se o formulário de login foi enviado
        if request.form.get("SendLogin"):
            form_data = request.form.to_dict() # Cria uma cópia mutável do dicionário
            session["user_email"] = form_data["user"] #armazena o email do suario na sessao
            del(form_data["SendLogin"]) # Remove o campo "SendLogin" do formulário para evitar enviar dados indesejados

            #valor padrão da condition como true
            condition = True

            # Verifica se todos os campos do formulário foram preenchidos
            for camp in form_data:
                if not form_data[camp]:
                    condition = False

            # Verifica se as credenciais de login são válidas, caso não retorna uma mensagem de erro
            if condition:
                if self.login.verify_login(form_data):
                    if self.login.verify_user_sit():
                        return redirect(url_for("main_routes.route_method", route_name="dashboard", method="index"))

                    #Caso o usuario esteja com a conta inativada, renderiza a página de login com uma mensagem de erro
                    form_data["error_message"] = "This account was desactivated!"
                    return template_render("login.html", **form_data)

                # Caso o login falhe, armazena a mensagem de erro na sessão e redireciona para a página de login
                form_data["error_message"] = session["error_message"]
                del(session["error_message"])
                return template_render("login.html", **form_data)

            #Caso os campos não sejam devidamente preenchidos, renderiza a página de login com uma mensagem de erro
            form_data["error_message"] = "All fields must be filled in!"
            return template_render("login.html", **form_data)
        
        #  Se o formulário de login não foi enviado, verifica se há uma autorização na sessão

        else:
            if 'Authorize' in session:
                authorize = session['Authorize'] #armazena o valor da flag Authorize na sessao
                
                del session['Authorize'] # Remove a autorização da sessão após o uso

                # Renderiza a página de login com o status de autorização
                return template_render("login.html", authorize=authorize)

            if 'Change_password' in session:
                change = session['Change_password'] #armazena o valor da flag Authorize na sessao
                
                del session['Change_password'] # Remove a autorização da sessão após o uso

                # Renderiza a página de login com o status de autorização
                return template_render("login.html", Change_password=change)
            #Caso não haja autorização na sessão, renderiza a página de login sem a flag
            return template_render("login.html")
