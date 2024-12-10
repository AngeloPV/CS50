from flask import session, redirect, url_for
class Logout:
    """
    Classe responsavel por realizar o logout do usuario, finalizando todas as suas sessoes e redirecionando
    para a página de login novamente
    """
    def index(self):
        session.clear()  

        return redirect(url_for("main_routes.route_method", route_name="login", method="index"))