from flask import Flask, render_template, request
import os, sys, matplotlib

matplotlib.use('Agg')

# Adiciona o caminho do diretório pai para importações dos módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.plot_creator import Plot_Creator
from controllers.get_crypto_data import GetCryptoData

USER_ID = 1

app = Flask(__name__)

#Classe responsavel por exibir o dashboard
class Dashboard:
    def __init__(self):
        self.data = GetCryptoData() #Cria uma instancia da classe responsavel pelos dados do usuário/cripto
        self.dashboard = Plot_Creator() #Cria uma instancia da classe responsavel por gerar os graficos
    def get_default_data(self):
        #Função para obter os dados padrão para Bitcoin.
        return {
            'plot_url': 'static/images/dashboard/bitcoin.png',
            'history_plot_url': f'static/images/dashboard/crypto_history_1_{USER_ID}.png',
            'title': "Bitcoin",
            'volume': self.data.get_volume('bitcoin'),
            'spent_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_spent_{USER_ID}_1.png'),
            'spent_plot_data': self.dashboard.create_plot_spent(user_id=USER_ID, time='1')[1],
            'last_buy_date': self.data.get_last_buy_date(USER_ID),
            'last_trade_data': self.data.get_last_trade_data(USER_ID)
        }

    def get_crypto_data(self, crypto_name):
        #Função para obter os dados baseados na criptomoeda selecionada
        crypto_id = 1 if crypto_name == 'bitcoin' else 2
        self.dashboard.create_plot_range_value(crypto_name)
        self.dashboard.create_plot_history(crypto_id, USER_ID)
        return {
            'plot_url': os.path.join('static', 'images', 'dashboard', f'{crypto_name}.png'),
            'history_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_history_{crypto_id}_{USER_ID}.png'),
            'title': crypto_name.capitalize(),
            'volume': self.data.get_volume(crypto_name)
        }

    def update_spent_plot(self, total_spent):
        #Atualiza o gráfico de gastos com base no valor total gasto
        return {
            'spent_plot_url': os.path.join('static', 'images', 'dashboard', f'crypto_spent_{USER_ID}_{total_spent}.png'),
            'spent_plot_data': self.dashboard.create_plot_spent(user_id=USER_ID, time=total_spent)[1]
        }


##usar blueprint qnd juntar
show_dashboard = Dashboard()

@app.route('/', methods=['GET', 'POST'])
def index():
    data = show_dashboard.get_default_data()

    if request.method == 'POST':
        crypto_name = request.form.get('crypto') #verifica se foi pressionado   
        total_spent = request.form.get('total_spent', '1') 
        if crypto_name:
            data.update(show_dashboard.get_crypto_data(crypto_name))  #altera o grafico entre btc-eth

        if total_spent:
            data.update(show_dashboard.update_spent_plot(total_spent)) #altera o total spent entre 1 mes, 6 meses e ao todo


    return render_template('dashboard.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
