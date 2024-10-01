from ...renderer import template_render

class Faq:
    @staticmethod
    def index():
        return template_render('faq.html')


