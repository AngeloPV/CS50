from flask import request, session, redirect, url_for
from ...renderer import template_render

from ...models.Authenticate_account_user import Authenticate_account_user


class Verify_code():
    def __init__(self):
        self.authenticate = Authenticate_account_user()

    #usuario digita o código
    def verify(self):
        if request.method == 'POST':
            #armazena todos os digitos na lista user_code
            user_code = ''
            for c in range(1, 7):
                digit = (request.form.get(f'digit-{c}'))
                user_code += digit

            login = request.form.get('login')

            # se o codigo estiver correto leva pra update_data com o parametro verified: true
            if session['code'] == user_code.upper():

                if login == 'True':
                    if self.authenticate.update_account(session["user_authentication_id"]):
                        del(session["user_authentication_id"])

                        session['Authorize'] = True
                        return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
                    
                    session['Authorize'] = False
                    return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
            
                data = {"verified": True, 
                        "to_update": session.get('to_update')}
                
                #limpa a sessao do code
                session.pop('code', None)
                return template_render('update_data.html', **data)
                
            else:
                data = {"msg": "Invalid code"}
                return template_render('verify.html', **data)

        return template_render('verify.html')
        