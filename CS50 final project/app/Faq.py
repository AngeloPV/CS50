from flask import Flask, render_template

class Faq:
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('faq.html')

    if __name__ == '__main__':
        app.run(debug=True)

faq = Faq()