from flask import render_template, request
from ..renderer import template_render

class Teste:
    @staticmethod
    def teste(parameter):
        name = request.args.get("name", parameter)
        return render_template("index.html", name=parameter)
