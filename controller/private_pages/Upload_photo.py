from flask import request, session, redirect, url_for
from ...renderer import template_render
from base64 import b64encode
from ..protected_pages.user_data import User_data
import os
from PIL import Image
from io import BytesIO



class Upload_photo:
    def __init__(self):
        self.user_data = User_data()

    def index(self):
        if request.method == 'POST':
            #pega o envio do arquivo
            file = request.files['profilePic']
            
            if file:
                #abre a imagem pra contar os pixels
                image = Image.open(file)
                
                #verifica as dimensões da imagem
                if image.size[0] < 350 or image.size[1] < 350:
                    data = {"msg": 'A imagem deve ter no minimo 350x350 pixels'}
                    return template_render('upload_photo.html', **data)
                
                if image.size[0] > 1920 or image.size[1] > 1080 :
                    data = {"msg": 'A imagem deve ter no máximo 1920x1080 pixels'}
                    return template_render('upload_photo.html', **data)
                
                #tira a transparencia
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                #redimensiona a imagem pra 350x350 mantem as proporçoes
                image.thumbnail((350, 350))
                
                #cria uma instancia da classe BytesIO e salva o objeto nela, dps pega os bytes
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG', qauality=65)  
                img_byte_arr = img_byte_arr.getvalue()

                #transofrma os bytes em base 64 pra adicionar no banco
                img_b64 = b64encode(img_byte_arr).decode('utf-8')
                img_src = f"data:image/jpeg;base64,{img_b64}"

                #adiciona a imagem no banco
                self.user_data.set_profile_img(img_src, session.get('user_id'))

                #coloca a imagem atualizada na sessao
                img_bd = self.user_data.get_profile_img(session.get('user_id'))
                session['profile_img'] = img_bd

                return redirect(url_for("main_routes.route_method", route_name="dashboard", method="index"))
            data = {"msg": "Escolha um arquivo"}
            return template_render('upload_photo.html', **data)

        return template_render('upload_photo.html')

