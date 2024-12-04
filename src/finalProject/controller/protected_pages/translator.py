from transformers import MarianMTModel, MarianTokenizer
from huggingface_hub import login

def login():
    login(token='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')
    return True

# Seu token de acesso
token = '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'

# Inicializar o modelo de tradução (MarianMT)
src_lang = 'pt'  # Idioma de origem (português)
tgt_lang = 'en'  # Idioma de destino (inglês)
model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'

# Carregar o modelo com autenticação
model = MarianMTModel.from_pretrained(model_name, use_auth_token=token)
tokenizer = MarianTokenizer.from_pretrained(model_name, use_auth_token=token)

# Função de tradução
def translate(text, source_lang='pt', target_lang='en'):
    # Tokenizar o texto
    tokens = tokenizer.encode(text, return_tensors='pt', padding=True)
    # Traduzir
    translation = model.generate(tokens, max_length=100)
    # Decodificar a tradução
    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)
    return translated_text
