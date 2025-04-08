from flask import session, request, redirect, url_for
from ...models.User import User
from ...renderer import template_render
class Delete_account:
    """
    Classe responsavel por desativar a conta do usuario, altera a situação da conta para 0 (desativada) e
    impossibilita o acesso ao sistema para o usuario, no entanto seus dados  e operações permannecem no banco
    """
    def __init__(self):
        self.user_data = User() #intancia a classe responsavel pelos dados do usuario
    def index(self):
        """
        Faz duas verificacoes pelo javascript e só então finaliza todas as sessoes e desativa a conta do
        usuario
        """
        if request.method == 'POST':
            confirmation = request.form.get('confirmation')
            if confirmation == 'yes':
                self.user_data.delete_account(user_id=session.get('user_id'))
                session.clear()

                
                return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
        else:
            return template_render('account.html')