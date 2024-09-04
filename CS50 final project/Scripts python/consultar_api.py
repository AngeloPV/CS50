import requests
import json

url = 'https://api.coingecko.com/api/v3/coins/markets'
params = {
    'vs_currency': 'usd',
    'ids': 'bitcoin,ethereum'
}
response = requests.get(url, params=params)
data = response.json()

# Imprime os dados formatados (indenta a resposta para melhor visualização)
print(json.dumps(data, indent=4))