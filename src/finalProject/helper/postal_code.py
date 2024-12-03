import requests
from flask import request
class Postal_code():
    def get_zip_code_from_coordinates(self, lat, lon):
                url = "https://nominatim.openstreetmap.org/reverse"
                params = {
                    'lat': lat,
                    'lon': lon,
                    'format': 'json',
                    'addressdetails': 1
                }
                headers = {
                    'User-Agent': 'AF Crypto/ (felipesssoapro@gmail.com)'  # Modifique com o seu nome ou nome do app
                }
                response = requests.get(url, params=params, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    return data.get('address', {}).get('postcode', None)
                return None
    
    def get_coordinates_from_json(self):
        if request.is_json:
            data = request.get_json()  # Tenta pegar os dados JSON
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            print(data, '-'*99)
            if latitude and longitude:
                print(latitude, longitude, '-'*99)
                # Exemplo de lógica para obter o CEP com base na latitude e longitude
                cep = self.get_zip_code_from_coordinates(latitude, longitude)
                return cep
            return None
        
    def get_city_state_country(self, cep):
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'postalcode': cep,
            'format': 'json',
            'addressdetails': 1,
        }
        headers = {
            'User-Agent': 'AF Crypto/ (felipesssoapro@gmail.com)'  
        }
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            if results:
                # Pega o primeiro resultado da busca
                address = results[0].get('address', {})
               
                return {
                    'cidade': address.get('municipality', None),
                    'estado': address.get('state', None),
                    'pais': address.get('country', None)
                }
            return {'error': 'Endereço não encontrado para o CEP fornecido'}
        return {'error': f'Erro na requisição: {response.status_code}'}
