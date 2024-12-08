from flask import request, session
from ...renderer import template_render
from ...models.Resend_authenticate import Resend_authenticate

class Resend_authentication_email:
    """
    Classe responsável pelo processo de reenvio de email de autenticação.
    Ela valida o formulário enviado pelo usuário e, dependendo do resultado, 
    reenvia o email ou exibe uma mensagem de erro.
    """
    
    def __init__(self):
       
        self.resend = Resend_authenticate()  # Instância da classe Resend_authenticate para validar e reenviar o email.

    def index(self):
        """
        Processa o formulário enviado pelo usuário para reenvio de email de autenticação.
        Verifica se todos os campos foram preenchidos e se o email é válido. Caso a validação
        seja bem-sucedida, o sistema reenviará o email ou exibirá uma mensagem de erro.

        Retorna: Renderiza a página de reenvio de email com a mensagem de erro ou sucesso.
        """
        
        # Verifica se o formulário de reenvio foi enviado
        if request.form.get("ResendAuthorize"):
            form_data = request.form.to_dict()  # Cria uma cópia mutável do dicionário de dados do formulário
            del(form_data["ResendAuthorize"])  # Remove o campo "ResendAuthorize" do formulário para evitar enviar dados indesejados

            condition = True  # Inicializa uma variável de controle para validar os campos
            for camp in form_data:
                if not form_data[camp]:
                    condition = False  # Se algum campo estiver vazio, a condição será falsa

            # Se todos os campos estiverem preenchidos
            if condition:
                # Verifica se o email fornecido é válido e se o reenvio foi bem-sucedido
                if self.resend.verify_email(form_data):
                    # Se o email for válido, renderiza a página de verificação com sucesso
                    return template_render("verify.html", register_email=True)

                # Se ocorrer um erro de validação, exibe uma mensagem de erro e renderiza a página de reenvio
                elif "error_validate" in session:
                    form_data["error_message"] = session["error_validate"]
                    del(session["error_validate"])  # Remove a mensagem de erro da sessão
                    return template_render("resend_authentication_email.html", **form_data)

                # Se ocorrer um erro ao tentar enviar o email, exibe uma mensagem de erro
                elif "error_send_email" in session:
                    form_data["error_message"] = session["error_send_email"]
                    del(session["error_send_email"])  # Remove a mensagem de erro da sessão
                    return template_render("resend_authentication_email.html", **form_data)
            else:
                # Se algum campo estiver vazio, exibe uma mensagem de erro
                form_data["error_message"] = "All fields must be filled in!"
                return template_render("resend_authentication_email.html", **form_data)
        
        # Se o formulário de reenvio não foi enviado, renderiza a página de reenvio de email sem parâmetros
        return template_render("resend_authentication_email.html")
