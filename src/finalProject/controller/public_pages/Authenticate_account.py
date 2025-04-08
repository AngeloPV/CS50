from flask import request, redirect, url_for, session

from ...models.Authenticate_account_user import Authenticate_account_user


class Authenticate_account:
    """
    Classe responsavel por gerenciar a autenticação e atualização de informações
    """
    def __init__(self):
        self.account_user = Authenticate_account_user() #cria uma instancia responsavel pra autenticação

    def index(self, conf_email):
        """
        Funcao responsavel por verificar se o usuario esta com a conta autorizada, caso sim,
        adiciona a flag Authorize na sessao e redireciona pra pagina de login
        Caso contrario, redireciona para a pagina de login sem a flag Authorize na sessao

        Parametros:
            conf_email (str): email do usuario
        """
        if conf_email:
            if self.account_user.get_data_user(conf_email):
                session["Authorize"] = True
                return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))

            session["Authorize"] = False
            return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))
        
        session["Authorize"] = False
        return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))
