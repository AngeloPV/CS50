from flask import session, request, redirect, url_for
from ..protected_pages.user_data import User_data
from ...renderer import template_render
class Delete_account:
    def __init__(self):
        self.user_data = User_data()
    def index(self):
        if request.method == 'POST':
            confirmation = request.form.get('confirmation')
            if confirmation == 'yes':
                session.clear()  
                self.user_data.delete_account(user_id=session.get('user_id'))
                return redirect(url_for("main_routes.route_method", route_name="login", method="index"))
        else:
            return template_render('account.html')