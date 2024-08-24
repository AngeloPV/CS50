from flask import Flask, render_template, request
import os, sys, matplotlib

matplotlib.use('Agg')

# Adiciona o caminho do diretório pai para importações dos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.dashboard import create_plot, create_plot_history, create_plot_spent
from controllers.get_crypto_data import get_volume, get_last_buy_date, get_last_trade_data

USER_ID = 1

app = Flask(__name__)

def get_default_data():
    #Função para obter os dados padrão para Bitcoin.
    return {
        'plot_url': 'static/images/dashboard/bitcoin.png',
        'history_plot_url': f'static/images/dashboard/crypto_history_1_{USER_ID}.png',
        'title': "Bitcoin",
        'volume': get_volume('bitcoin'),
        'spent_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_spent_{USER_ID}_1.png'),
        'spent_plot_data': create_plot_spent(user_id=USER_ID, time='1')[1],
        'last_buy_date': get_last_buy_date(USER_ID),
        'last_trade_data': get_last_trade_data(USER_ID)
    }

def get_crypto_data(crypto_name):
    #Função para obter os dados baseados na criptomoeda selecionada
    crypto_id = 1 if crypto_name == 'bitcoin' else 2
    create_plot(crypto_name)
    create_plot_history(crypto_id, USER_ID)
    return {
        'plot_url': os.path.join('static', 'images', 'dashboard', f'{crypto_name}.png'),
        'history_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_history_{crypto_id}_{USER_ID}.png'),
        'title': crypto_name.capitalize(),
        'volume': get_volume(crypto_name)
    }

def update_spent_plot(total_spent):
    #Atualiza o gráfico de gastos com base no valor total gasto
    return {
        'spent_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_spent_{USER_ID}_{total_spent}.png'),
        'spent_plot_data': create_plot_spent(user_id=USER_ID, time=total_spent)[1]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    # Dados padrão (Bitcoin)
    data = get_default_data()

    if request.method == 'POST':
        crypto_name = request.form.get('crypto')
        total_spent = request.form.get('total_spent', '1')  # Padrão para '1' se não for especificado

        if crypto_name:
            data.update(get_crypto_data(crypto_name))

        if total_spent:
            data.update(update_spent_plot(total_spent))

    return render_template('dashboard.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
