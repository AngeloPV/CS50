from flask import request, redirect, url_for
from ...renderer import template_render



class Language:
    """
    Classe responsavel por alterar o idioma do site
    """

    def index(self):
        """
        Renderiza um form com os idiomas disponiveis para serem escolhidos pelo usuario
        """
        #linguagens disponiveis
        languages = ['english']
        if request.method == 'POST':
            #pega o valor do form
            language = request.form.get('language')

            #verifica se esta vazio
            if not language:
                msg = 'Invalid language'
                data = {
                "languages": languages, "error_message":msg
                }
                return template_render('language.html', **data)
            
            #verifica se a linguagem escolhido é valido
            if language.lower() not in languages:
                msg = 'Invalid language'
                data = {
                "languages": languages, "error_message":msg
                }
                return template_render('language.html', **data)
            
            data = {'authorize': 'Language successfully updated!', 'redirect_url': url_for("main_routes.route_method", route_name="account", method="index")}
            return redirect(url_for("main_routes.route_method", route_name="account", method='index', **data))

        #renderiza as linguagens e o form
        data = {'languages': languages}
        return template_render('language.html', **data)