from flask import session, redirect, url_for

class Logout:

    def index(self):
        session.clear()  
        return redirect(url_for("main_routes.route_method", route_name="login", method="index"))