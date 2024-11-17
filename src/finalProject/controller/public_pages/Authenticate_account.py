from flask import request, redirect, url_for, session

from ...models.Authenticate_account_user import Authenticate_account_user


class Authenticate_account:
    def __init__(self):
        self.account_user = Authenticate_account_user()
        # Inicialize qualquer atributo necessário aqui

    def index(self, conf_email):
        if conf_email:
            if self.account_user.get_data_user(conf_email):
                session["Authorize"] = True
                return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))

            session["Authorize"] = False
            return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))
        
        session["Authorize"] = False
        return redirect(url_for("main_routes.route_method", route_name="Login", method="index"))
