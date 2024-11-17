from flask import request, session, redirect, url_for
from ...renderer import template_render
from ...helper.helper_select import Select
from ...helper.helper_update import Update

from ..protected_pages.user_data import User_data


class Theme:
    def __init__(self):
        self.select = Select()
        self.update = Update()
        self.user_data = User_data()


    def index(self):
        themes = ['light-theme', 'dark-theme']
        if request.method == 'POST':
            theme = request.form.get('theme')

            if not theme:
                msg = 'Invalid theme'
                data = {
                "themes": themes, "error_message":msg
                }
                return template_render('theme.html', **data)
            
            if theme.lower() not in themes:
                msg = 'Invalid theme'
                data = {
                "themes": themes, "error_message":msg
                }
                return template_render('theme.html', **data)
            
            
                
            self.user_data.set_theme(user_id=session.get('user_id'), theme=theme)
            session['theme'] = self.user_data.get_theme(user_id=session.get('user_id'))
            return redirect(url_for("main_routes.route_method", route_name="account", method="index"))

        data = {'themes': themes}
        return template_render('theme.html', **data)