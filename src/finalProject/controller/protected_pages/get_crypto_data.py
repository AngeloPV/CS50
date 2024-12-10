import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ...models.dashboard_data import Dashboard_data
from ...models.update_criptocurrencies import CryptoUpdate

class GetCryptoData:
    """
    Classe responsavel por pegar os dados relacionados as criptomoedas e atualizar o banco de dados das
    mesmas
    """
    def __init__(self):
        self.dashboard = Dashboard_data() #cria uma instancia responsavel pra inserir dados no banco
        self.update = CryptoUpdate() #cria uma instancia responsavel pra atualizar dados do banco

    def format_volume(self, volume):
        """
        Função responsavel por formata o volume em uma forma legível como '5M', '32k', '6.6B', etc.
        """
        if volume >= 1_000_000_000:
            return f"{volume / 1_000_000_000:.1f}B"
        elif volume >= 1_000_000:
            return f"{volume / 1_000_000:.1f}M"
        elif volume >= 1_000:
            return f"{volume / 1_000:.1f}k"
        else:
            return str(volume)

    #pega os dados da api dos ultimos 6 meses
    def get_cripto_data(crypto_name):
        """
        Pega os dados das criptomoedas nos ultimos 6 meses por meio da API Coingecko,
        para serem exibidos no dashboard

        Parametros:
            crypto_name (str): Nome da criptomoeda

        Retorno:
            dict: Dicionario com os dados das criptomoedas
        """

        url = f'https://api.coingecko.com/api/v3/coins/{crypto_name}/market_chart'
        params = {
            'vs_currency': 'usd',
            'days': '180',
            'interval': 'daily'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # verifica se houve algum erro na solicitação
            data = response.json()

            prices = data.get('prices', [])
            total_volumes = data.get('total_volumes', [])

            # armazena os valores dos dias referente ao mes no dicionario
            periods = {
                "price_6_months_ago": 0,     # 180 dias atrás
                "price_5_months_ago": 30,    # aproximadamente 150 dias atrás
                "price_4_months_ago": 60,    # aproximadamente 120 dias atrás
                "price_3_months_ago": 90,    # aproximadamente 90 dias atrás
                "price_2_months_ago": 120,   # aproximadamente 60 dias atrás
                "price_1_month_ago": 150,    # aproximadamente 30 dias atrás
                "price_7_days_ago": -8,      # 7 dias atrás
                "price_1_day_ago": -2,       # 1 dia atrás
                "current_price": -1          # preço atual
            }

            def get_price_at_index(index, default=None):
                """Retorna o preço no índice especificado ou um valor padrão."""
                try:
                    return prices[index][1]
                except IndexError:
                    return default

            # pega os indices referente aos dias e armazena o valor da moeda naquele dia 
            price_data = {key: get_price_at_index(index) for key, index in periods.items()}
            print(price_data)
            return price_data
        
        #caso dê algum erro na requisição, retorna o erro
        except requests.RequestException as e:
            return {"error": str(e)}


    def get_crypto_data_for_buy(self, crypto_names):
        """
        Função responsavel por pegar os dados das criptomoedas por meio da API Coingecko para serem utilizados
        na página de compra, a diferença dessa para a get_cripto_data é que essa pega os dados de várias moedas
        simultaneamente
        """
        #url da api com varias moedas
        api_url = "https://api.coingecko.com/api/v3/coins/markets"

        # converte a lista de moedas em uma string separada por vírgulas
        crypto_names_str = ','.join(crypto_names)
        
        try:
            #requisita varias moedas ao msm tempo
            params = {
                'vs_currency': 'usd',
                'ids': crypto_names_str  
            }
            response = requests.get(api_url, params=params)
            response.raise_for_status()  
            data = response.json()

            # organiza os dados para cada moeda
            result = {}
            for crypto in data:
                result[crypto['id']] = {
                    'name': crypto.get('name', 'N/A'),
                    'symbol': crypto.get('symbol', 'N/A').upper(),
                    'current_price': crypto.get('current_price', 'N/A'),
                    'volume_24h': self.format_volume(crypto.get('total_volume', 0)),#pega o volume formatado
                    'status': True if crypto['id'] in ['bitcoin', 'ethereum'] else False,
                    'price_change_percentage_24h': crypto.get('price_change_percentage_24h', 'N/A') 

                }

            return result

        except requests.RequestException as e:
            return {"error": str(e)}
                        
    #chama a funcao no valor referente a moeda
    crypto_data = {
        "bitcoin": get_cripto_data('bitcoin'),
        "ethereum": get_cripto_data('ethereum')
    }

    #atualiza o banco com o valor atual das moedas
    def do_update_database(self):
        """
        Atualiza o banco com o valor atual das moedas
        """
        self.update.update_database(self.crypto_data)  

    def get_crypto_buy(self, crypto_id, user_id):
        """
        Pega os dados de compra do usuário
        """
        return self.dashboard.get_crypto_buy(crypto_id=crypto_id, user_id=user_id)

    def get_total_spent(self, user_id, time): 
        """
        Pega o total gasto pelo usuário
        """
        return self.dashboard.get_total_spent(time=time, user_id=user_id)

 
    
    