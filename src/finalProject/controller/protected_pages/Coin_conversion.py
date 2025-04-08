import requests

class Coin_conversion: 
    _api_data = None  
    
    def __init__(self):
        if Coin_conversion._api_data is None:
            url = "https://api.coingecko.com/api/v3/simple/price"

            params = {
                "ids": "ethereum",
                "vs_currencies": "btc"
            }

            response = requests.get(url, params=params)
            Coin_conversion._api_data = response.json()

        self.eth_to_btc = Coin_conversion._api_data["ethereum"]["btc"]


    def get_btc(self, coin_amount):
        print(f"1 ETH = {self.eth_to_btc} BTC")

        # Calculando o valor em BTC
        btc_amount = coin_amount * self.eth_to_btc

        return round(btc_amount, 3)


    def get_eth(self, coin_amount):
        # Obtendo o valor de BTC em ETH
        btc_to_eth = 1 / self.eth_to_btc

        eth_amount = coin_amount * btc_to_eth

        return round(eth_amount, 3)


    @classmethod
    def clear_data(cls):
        cls._api_data = None