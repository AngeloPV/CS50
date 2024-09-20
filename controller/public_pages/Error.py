from ...renderer import template_render


class Error():
    # @main_routes.errorhandler(404)
    def show_error(self, msg_error, type_error):
       return template_render("error.html", error=msg_error), type_error
    



#from flask import render_template
# from blueprints.errors import errors_bp

# def setup_error_handlers(app):
#     @app.errorhandler(404)
#     def not_found_error(error):
#         return render_template("404.html", error="Page not found"), 404

#     @app.errorhandler(500)
#     def internal_error(error):
#         return render_template("500.html", error="Internal server error"), 500

#     @app.errorhandler(400)
#     def bad_request_error(error):
#         return render_template("400.html", error="Bad request"), 400
