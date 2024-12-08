from flask import request, session, redirect, url_for
from ...renderer import template_render
from ...helper.helper_select import Select
from ...helper.helper_update import Update

from ..protected_pages.user_data import User_data


class Theme:
    """
    Classe responsavel por alterar o tema do site
    """
    def __init__(self):
        self.select = Select() #cria uma instancia responsavel pra resgatar dados do banco
        self.update = Update() #cria uma instancia responsavel pra atualizar dados do banco
        self.user_data = User_data() #cria uma instancia da classe responsavel pelos dados do usuário


    def index(self):
        """
        Renderiza um form com os temas disponiveis para serem escolhidos pelo usuario
        """
        #temas disponiveis
        themes = ['light-theme', 'dark-theme']
        if request.method == 'POST':
            #pega o valor do form
            theme = request.form.get('theme')

            #verifica se esta vazio
            if not theme:
                msg = 'Invalid theme'
                data = {
                "themes": themes, "error_message":msg
                }
                return template_render('theme.html', **data)
            
            #verifica se o tema escolhido é valido
            if theme.lower() not in themes:
                msg = 'Invalid theme'
                data = {
                "themes": themes, "error_message":msg
                }
                return template_render('theme.html', **data)
            
            #atualiza o tema e armazena na sessao
            self.user_data.set_theme(user_id=session.get('user_id'), theme=theme)
            session['theme'] = self.user_data.get_theme(user_id=session.get('user_id'))
    
            data = {'authorize': 'Theme successfully updated!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
            return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))

        #renderiza os temas e o form
        data = {'themes': themes}
        return template_render('theme.html', **data)