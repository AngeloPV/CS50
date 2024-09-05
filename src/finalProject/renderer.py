from flask import render_template

def template_render(file_name, **data):

    return render_template(file_name, **data)
