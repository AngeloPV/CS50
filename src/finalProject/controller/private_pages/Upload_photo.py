from flask import request, session, redirect, url_for
from ...renderer import template_render
from werkzeug.utils import secure_filename
from PIL import Image  # Pillow para manipulação de imagens
from ..protected_pages.user_data import User_data
import os


class Upload_photo:
    def __init__(self):
        self.user_data = User_data()

    def index(self):
        if request.method == 'POST':
            # Pega o envio do arquivo
            file = request.files['profilePic']
            
            if file:
                filename = secure_filename(file.filename)
                file_extension = os.path.splitext(filename)[1]  # Obtém a extensão do arquivo (ex: .jpg, .png)

                # Apenas aceitamos imagens nos formatos suportados
                if file_extension.lower() not in ['.png', '.jpg', '.jpeg', '.webp']:
                    data = {"msg": "Formato de imagem não suportado. Apenas .jpg e .png são permitidos."}
                    return template_render('upload_photo.html', **data)

                # Define o nome do novo arquivo
                new_filename = f'profile_image_user_{session.get("user_id")}{file_extension}'
                current_dir = os.path.dirname(__file__)
                save_dir = os.path.join(current_dir, '..', '..', 'static', 'images', 'users')
                os.makedirs(save_dir, exist_ok=True)
                file_path = os.path.join(save_dir, new_filename)

                # Abre a imagem usando PIL
                image = Image.open(file)

                # Verifica o tamanho da imagem
                width, height = image.size
                if width < 150 or height < 150:
                    data = {"msg": "Imagem muito pequena. O tamanho mínimo é 150x150 pixels."}
                    return template_render('upload_photo.html', **data)

                if width > 1280 or height > 720:
                    data = {"msg": "Imagem muito grande. O tamanho máximo é 1280x720 pixels."}
                    return template_render('upload_photo.html', **data)


                image.thumbnail((500, 500))

                format=file_extension[1:].upper()
                image.save(file_path, format=format)  

                # Salva o nome da imagem no banco de dados
                self.user_data.set_profile_img(img=new_filename, user_id=session.get("user_id"))

                return redirect(url_for("main_routes.route_method", route_name="dashboard", method="index"))

            data = {"msg": "Escolha um arquivo"}
            return template_render('upload_photo.html', **data)

        return template_render('upload_photo.html')
