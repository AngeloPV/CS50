from flask import request, session, redirect, url_for
from ...renderer import template_render
from ...models.Authenticate_account_user import Authenticate_account_user

class Verify_code:
    """
    Classe responsável pela verificação do código de autenticação fornecido pelo usuário.
    Ela valida o código digitado e, dependendo do resultado, atualiza a conta do usuário ou redireciona para uma página de erro.

    """
    
    def __init__(self):
        self.authenticate = Authenticate_account_user() # Instância responsavel por autenticar a conta do usuário.

    def verify(self):
        """
        Verifica o código de autenticação enviado pelo usuário no formulário. Se o código estiver correto,
        o processo de verificação continua e, dependendo do caso, a conta do usuário será atualizada ou o
        sistema redirecionará para a página de login.

        Retorna: Se o código for válido, redireciona para a página de login ou para a página de atualização de dados.
                Se o código for inválido, renderiza a página de verificação com uma mensagem de erro.
        """
        
        if request.method == 'POST':
            user_code = ''  # Inicializa uma variável para armazenar o código fornecido pelo usuário

            # Concatena os 6 dígitos do código inserido pelo usuário
            for c in range(1, 7):
                digit = request.form.get(f'digit-{c}')
                user_code += digit

            login = request.form.get('login')  # Obtém o valor do campo 'login'
            Recover = request.form.get('Recover')  # Obtém o valor do campo 'Recover'

            # Se o código fornecido pelo usuário for igual ao código armazenado na sessão
            if session['code'] == user_code.upper():
                if Recover == 'True':
                    return redirect(url_for("main_routes.route_method", route_name="Change_password", method="index", parameter=session['code']))

                if login == 'True':
                    # Se o usuário já está logado e a conta foi atualizada com sucesso
                    if self.authenticate.update_account(session["user_authentication_id"]):
                        del(session["user_authentication_id"])  # Remove o ID de autenticação da sessão

                        session['Authorize'] = True  # Marca a conta como autorizada
                        session.pop('code', None) # Limpa o código de autenticação da sessão
                        return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
                    
                    # Caso a atualização da conta falhe, marca a conta como não autorizada
                    session['Authorize'] = False
                    session.pop('code', None) # Limpa o código de autenticação da sessão
                    return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
                
                # Caso o código esteja correto e o login não seja 'True', o sistema prepara para renderizar a página de atualização de dados
                data = {"verified": True, 
                        "to_update": session.get('to_update')}
                
                # Limpa o código de autenticação da sessão
                session.pop('code', None)
                return template_render('update_data.html', **data)
                
            else:
                if Recover == 'True':
                    data = {"msg": "Invalid code"}
                    return template_render('verify.html', Recover_password=True, **data)
                
                if login == 'True':
                    data = {"msg": "Invalid code"}
                    return template_render('verify.html', register_email=True, **data)


                # Se o código estiver incorreto, exibe uma mensagem de erro
                data = {"msg": "Invalid code"}
                return template_render('verify.html', **data)

        # Se o método de requisição não for POST, renderiza a página de verificação
        return template_render('verify.html')
