from flask import request, redirect, url_for
from ..renderer import template_render

class Login:
    @staticmethod
    def index():
        if request.form.get("SendLogin"):
            User = request.form.get("User")
            password = request.form.get("Pass")

            data = {
                'User': User, 'password': password
            }

            count = 0
            for camp in data:
                if not data[camp]:
                    return template_render("login.html", data)
                elif count == len(data) - 1:
                    return template_render("index.html", data)
                count += 1

            # return redirect(url_for("main_routes.handle_route", route_name="register", paramenter="index", name=name))
        else:
            return template_render("login.html")
