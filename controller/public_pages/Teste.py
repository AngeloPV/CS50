from flask import render_template, request
from ...renderer import template_render

class Teste:
    @staticmethod
    def index():
        parameter = 'index'
        # name = request.args.get("name", parameter)
        return render_template("error.html", name=parameter)
