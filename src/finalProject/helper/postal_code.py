import requests
import re
from flask import request
class Postal_code:
    def get_zip_code_from_coordinates(self, lat, lon):
        """
        Obtém o CEP com base em coordenadas (latitude e longitude) usando a API Nominatim.

        Parâmetros:
            lat (float): Latitude da localização.
            lon (float): Longitude da localização.

        Retorna:
            str: CEP correspondente ou None se não for encontrado.
        """
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'addressdetails': 1
        }
        headers = {
            'User-Agent': 'AF Crypto/ (seu_email@gmail.com)'  # Modifique com seu email ou nome do app
        }
        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('address', {}).get('postcode', None)
        except requests.RequestException:
            pass
        return None

    def get_coordinates_from_json(self):
        """
        Obtém as coordenadas do corpo da requisição JSON e busca o CEP correspondente.

        Retorna:
            str: O CEP obtido das coordenadas ou None.
        """
        if request.is_json:
            data = request.get_json()  # Tenta obter os dados JSON
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if latitude and longitude:
                # Busca o CEP com base nas coordenadas
                cep = self.get_zip_code_from_coordinates(latitude, longitude)
                return cep
        return None
    
    def get_city_state_country(self, cep):
        if not cep:
            return None
        """
        Obtém informações da cidade, estado e país com base no CEP usando a API ViaCEP.
        
        Parâmetros:
            cep (str): O código postal a ser pesquisado.
        
        Retorna:
            dict: Dicionário com informações da cidade, estado e país.
        """
        # Formata o CEP para conter apenas números
        cep = re.sub(r"\D", "", cep)

        # Verifica se o CEP tem 8 dígitos
        if len(cep) != 8:
            return None

        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if "erro" not in data:
                    return {
                        'cidade': data.get('localidade'),
                        'estado': data.get('uf'),
                        'pais': 'Brasil'  # A API ViaCEP só cobre o Brasil
                    }
        except requests.RequestException:
            pass
        return None

    def is_valid_zip_code(self, cep):
        """
        Verifica se o CEP fornecido é válido usando a API ViaCEP.

        Parâmetros:
            cep (str): O código postal a ser validado.

        Retorna:
            bool: True se o CEP é válido, False caso contrário.
        """
        # Formata o CEP removendo caracteres não numéricos
        cep = re.sub(r"\D", "", cep)

        # Verifica se o CEP tem exatamente 8 dígitos
        if len(cep) != 8:
            return False

        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return "erro" not in data  # Retorna True se o CEP for válido
        except requests.RequestException:
            pass
        return False

    def format_zip_code(self, cep):
        """
        Formata um CEP no padrão 99999-999.
        
        Parâmetros:
            cep (str): O código postal a ser formatado.
        
        Retorna:
            str: O CEP formatado ou None se inválido.
        """
        # Remove caracteres não numéricos
        cep = re.sub(r"\D", "", cep)

        # Verifica se o CEP tem 8 dígitos
        if len(cep) == 8:
            return f"{cep[:5]}-{cep[5:]}"
        return None
