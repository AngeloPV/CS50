from libretranslatepy import LibreTranslateAPI 
import requests 

class Translate:
    @staticmethod
    def translate_text(text, target_language='en'):
        url = "https://libretranslate.com/translate"  # ou outro endpoint que você deseja usar
        payload = {
            "q": text,
            "source": "auto",  # você pode definir a língua de origem se souber
            "target": target_language,
            "format": "text"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
            translated = response.json()  # Extrai a resposta JSON
            return translated['translatedText']  # Retorna o texto traduzido
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return text  # Retorna o texto original em caso de erro
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return text  # Retorna o texto original em caso de erro